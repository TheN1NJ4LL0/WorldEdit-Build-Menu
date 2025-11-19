from endstone_worldedit.utils import command_executor
from endstone_worldedit.structure_utils import structure_load

command = {
    "paste": {
        "description": "Pastes the copied selection with optional transformations.",
        "permissions": ["worldedit.command.paste"]
    }
}

@command_executor("paste")
def handler(plugin, sender, args):
    # Debug logging
    plugin.logger.info(f"[PASTE DEBUG] Player: {sender.name}, Args received: {args}")
    plugin.logger.info(f"[PASTE DEBUG] Args type: {type(args)}, Args length: {len(args)}")

    player_uuid = sender.unique_id
    if player_uuid not in plugin.clipboard or not plugin.clipboard[player_uuid]:
        sender.send_message("There is nothing to paste. Use /copy first.")
        return False

    dimension = sender.dimension
    player_location = sender.location

    # Parse arguments for transformations
    rotation_degrees = 0
    flip_x = False
    flip_y = False
    flip_z = False
    offset_x = 0
    offset_y = 0
    offset_z = 0
    include_air = False
    paste_entities = False  # Not implemented yet
    paste_biomes = False    # Not implemented yet

    i = 0
    while i < len(args):
        arg = args[i]
        plugin.logger.info(f"[PASTE DEBUG] Processing arg[{i}]: '{arg}'")

        if arg == "-r" or arg == "--rotate":
            # Rotation flag
            plugin.logger.info(f"[PASTE DEBUG] Found rotation flag")
            if i + 1 < len(args):
                try:
                    rotation_degrees = int(args[i + 1])
                    plugin.logger.info(f"[PASTE DEBUG] Rotation value parsed: {rotation_degrees}")
                    # Normalize to 0, 90, 180, 270
                    rotation_degrees = rotation_degrees % 360
                    if rotation_degrees not in [0, 90, 180, 270]:
                        error_msg = "§cRotation must be in 90-degree increments (90, 180, 270)§r"
                        sender.send_message(error_msg)
                        plugin.logger.error(f"[PASTE ERROR] {error_msg}")
                        return False
                    i += 1
                except ValueError as e:
                    error_msg = f"§cInvalid rotation value: {args[i + 1]}§r"
                    sender.send_message(error_msg)
                    plugin.logger.error(f"[PASTE ERROR] {error_msg} - Exception: {e}")
                    return False
        elif arg == "-fx" or arg == "--flip-x":
            flip_x = True
        elif arg == "-fy" or arg == "--flip-y":
            flip_y = True
        elif arg == "-fz" or arg == "--flip-z":
            flip_z = True
        elif arg == "-o" or arg == "--offset":
            # Offset flag: -o x,y,z
            if i + 1 < len(args):
                try:
                    offset_parts = args[i + 1].split(',')
                    if len(offset_parts) == 3:
                        offset_x = int(offset_parts[0])
                        offset_y = int(offset_parts[1])
                        offset_z = int(offset_parts[2])
                    i += 1
                except ValueError:
                    sender.send_message("§cInvalid offset format. Use: -o x,y,z§r")
                    return False
        elif arg == "-a" or arg == "--air":
            include_air = True
        elif arg == "-e" or arg == "--entities":
            paste_entities = True
        elif arg == "-b" or arg == "--biomes":
            paste_biomes = True

        i += 1

    undo_entry = []
    plugin.redo_history[player_uuid] = []  # Clear redo history on new action

    copied_blocks = plugin.clipboard[player_uuid]

    # Calculate dimensions of clipboard for rotation
    if copied_blocks:
        min_x = min(b[0] for b in copied_blocks)
        max_x = max(b[0] for b in copied_blocks)
        min_y = min(b[1] for b in copied_blocks)
        max_y = max(b[1] for b in copied_blocks)
        min_z = min(b[2] for b in copied_blocks)
        max_z = max(b[2] for b in copied_blocks)

        width = max_x - min_x + 1
        height = max_y - min_y + 1
        length = max_z - min_z + 1
    else:
        sender.send_message("§cClipboard is empty§r")
        return False

    # Transform and prepare blocks
    blocks_to_change = []
    for relative_x, relative_y, relative_z, block_type, data_value in copied_blocks:
        # Skip air blocks unless include_air is set
        if not include_air and block_type == "minecraft:air":
            continue

        # Normalize to 0-based coordinates
        norm_x = relative_x - min_x
        norm_y = relative_y - min_y
        norm_z = relative_z - min_z

        # Apply rotation around Y-axis (vertical)
        if rotation_degrees == 90:
            # 90 degrees clockwise: (x, z) -> (length - z - 1, x)
            rot_x = length - norm_z - 1
            rot_z = norm_x
        elif rotation_degrees == 180:
            # 180 degrees: (x, z) -> (width - x - 1, length - z - 1)
            rot_x = width - norm_x - 1
            rot_z = length - norm_z - 1
        elif rotation_degrees == 270:
            # 270 degrees clockwise: (x, z) -> (z, width - x - 1)
            rot_x = norm_z
            rot_z = width - norm_x - 1
        else:
            rot_x = norm_x
            rot_z = norm_z
        rot_y = norm_y

        # Apply flips
        if flip_x:
            rot_x = (width if rotation_degrees in [90, 270] else width) - rot_x - 1
        if flip_y:
            rot_y = height - rot_y - 1
        if flip_z:
            rot_z = (width if rotation_degrees in [90, 270] else length) - rot_z - 1

        # Apply offset and convert to world coordinates
        target_x = int(player_location.x + rot_x + offset_x)
        target_y = int(player_location.y + rot_y + offset_y)
        target_z = int(player_location.z + rot_z + offset_z)

        blocks_to_change.append((target_x, target_y, target_z, block_type, data_value))

    affected_blocks = len(blocks_to_change)

    if affected_blocks == 0:
        sender.send_message("§cNo blocks to paste§r")
        return False

    # Store undo history first
    for x, y, z, _, _ in blocks_to_change:
        block = dimension.get_block_at(x, y, z)
        undo_entry.append((x, y, z, block.type, block.data))

    if player_uuid not in plugin.undo_history:
        plugin.undo_history[player_uuid] = []
    plugin.undo_history[player_uuid].append(undo_entry)

    # Execute asynchronously if the task is large
    if affected_blocks > plugin.plugin_config["async-threshold"]:
        plugin.tasks[player_uuid] = {"dimension": dimension, "blocks": blocks_to_change}
        msg = f"§aStarting async paste operation for {affected_blocks} blocks"
        if rotation_degrees > 0:
            msg += f" (rotated {rotation_degrees}°)"
        msg += "...§r"
        sender.send_message(msg)
    else:
        for x, y, z, block_type, data_value in blocks_to_change:
            block = dimension.get_block_at(x, y, z)
            block.set_type(block_type)
            if data_value is not None:
                block.set_data(data_value)
        msg = f"§aPaste complete ({affected_blocks} blocks affected"
        if rotation_degrees > 0:
            msg += f", rotated {rotation_degrees}°"
        msg += ")§r"
        sender.send_message(msg)
    return True
