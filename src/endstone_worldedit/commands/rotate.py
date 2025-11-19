from endstone_worldedit.utils import command_executor

command = {
    "rotate": {
        "description": "Rotates the selection around the Y-axis (vertical).",
        "permissions": ["worldedit.command.rotate"]
    }
}

@command_executor("rotate", selection_required=True)
def handler(plugin, sender, args):
    """Rotate the selection around the Y-axis.
    
    Args:
        plugin: WorldEdit plugin instance
        sender: Player executing the command
        args: Command arguments [degrees]
    """
    if len(args) < 1:
        sender.send_message("§cUsage: /rotate <degrees>§r")
        sender.send_message("§7Valid angles: 90, 180, 270, -90§r")
        return False
    
    try:
        degrees = int(args[0])
    except ValueError:
        sender.send_message("§cDegrees must be a number (90, 180, 270, -90)§r")
        return False
    
    # Normalize degrees to 0, 90, 180, 270
    degrees = degrees % 360
    if degrees not in [0, 90, 180, 270]:
        sender.send_message("§cRotation must be in 90-degree increments (90, 180, 270)§r")
        return False
    
    if degrees == 0:
        sender.send_message("§cNo rotation needed for 0 degrees§r")
        return False
    
    player_uuid = sender.unique_id
    pos1 = plugin.selections[player_uuid]['pos1']
    pos2 = plugin.selections[player_uuid]['pos2']
    
    dimension = sender.dimension
    
    # Calculate selection bounds
    min_x = min(pos1[0], pos2[0])
    max_x = max(pos1[0], pos2[0])
    min_y = min(pos1[1], pos2[1])
    max_y = max(pos1[1], pos2[1])
    min_z = min(pos1[2], pos2[2])
    max_z = max(pos1[2], pos2[2])
    
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    length = max_z - min_z + 1
    
    # Calculate center point
    center_x = (min_x + max_x) / 2.0
    center_z = (min_z + max_z) / 2.0
    
    # Copy all blocks from selection
    blocks = []
    for x in range(int(min_x), int(max_x) + 1):
        for y in range(int(min_y), int(max_y) + 1):
            for z in range(int(min_z), int(max_z) + 1):
                block = dimension.get_block_at(x, y, z)
                # Store relative to min corner
                rel_x = x - min_x
                rel_y = y - min_y
                rel_z = z - min_z
                blocks.append((rel_x, rel_y, rel_z, block.type, block.data))
    
    # Prepare undo
    undo_entry = []
    plugin.redo_history[player_uuid] = []  # Clear redo history
    
    # Store original state for undo
    for x in range(int(min_x), int(max_x) + 1):
        for y in range(int(min_y), int(max_y) + 1):
            for z in range(int(min_z), int(max_z) + 1):
                block = dimension.get_block_at(x, y, z)
                undo_entry.append((x, y, z, block.type, block.data))
    
    if player_uuid not in plugin.undo_history:
        plugin.undo_history[player_uuid] = []
    plugin.undo_history[player_uuid].append(undo_entry)
    
    # Clear the selection area first
    for x in range(int(min_x), int(max_x) + 1):
        for y in range(int(min_y), int(max_y) + 1):
            for z in range(int(min_z), int(max_z) + 1):
                block = dimension.get_block_at(x, y, z)
                block.set_type("minecraft:air")
    
    # Rotate and place blocks
    blocks_to_place = []
    for rel_x, rel_y, rel_z, block_type, data_value in blocks:
        # Apply rotation around center
        if degrees == 90:
            # 90 degrees clockwise: (x, z) -> (z, -x)
            new_rel_x = length - 1 - rel_z
            new_rel_z = rel_x
        elif degrees == 180:
            # 180 degrees: (x, z) -> (-x, -z)
            new_rel_x = width - 1 - rel_x
            new_rel_z = length - 1 - rel_z
        elif degrees == 270:
            # 270 degrees clockwise (90 counter-clockwise): (x, z) -> (-z, x)
            new_rel_x = rel_z
            new_rel_z = width - 1 - rel_x
        else:
            new_rel_x = rel_x
            new_rel_z = rel_z
        
        # Convert back to world coordinates
        world_x = int(min_x + new_rel_x)
        world_y = int(min_y + rel_y)
        world_z = int(min_z + new_rel_z)
        
        blocks_to_place.append((world_x, world_y, world_z, block_type, data_value))
    
    # Place rotated blocks
    affected_blocks = len(blocks_to_place)
    
    if affected_blocks > plugin.plugin_config["async-threshold"]:
        plugin.tasks[player_uuid] = {"dimension": dimension, "blocks": blocks_to_place}
        sender.send_message(f"§aRotating {affected_blocks} blocks by {degrees}° (async)...§r")
    else:
        for x, y, z, block_type, data_value in blocks_to_place:
            block = dimension.get_block_at(x, y, z)
            block.set_type(block_type)
            if data_value is not None:
                block.set_data(data_value)
        sender.send_message(f"§aRotated {affected_blocks} blocks by {degrees}°§r")
    
    # Update selection if dimensions changed
    if degrees in [90, 270]:
        # Swap width and length
        new_max_x = min_x + length - 1
        new_max_z = min_z + width - 1
        plugin.selections[player_uuid]['pos2'] = (new_max_x, max_y, new_max_z)
        sender.send_message(f"§7Selection updated to new dimensions§r")
    
    return True

