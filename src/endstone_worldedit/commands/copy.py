from endstone_worldedit.utils import command_executor
from endstone_worldedit.structure_utils import structure_save

command = {
    "copy": {
        "description": "Copies the selection with optional flags.",
        "permissions": ["worldedit.command.copy"]
    }
}

@command_executor("copy", selection_required=True, area_check=False)
def handler(plugin, sender, args):
    # Debug logging
    plugin.logger.info(f"[COPY DEBUG] Player: {sender.name}, Args received: {args}")
    plugin.logger.info(f"[COPY DEBUG] Args type: {type(args)}, Args length: {len(args)}")

    # Parse flags
    include_air = False
    copy_entities = False
    copy_biomes = False

    i = 0
    while i < len(args):
        arg = args[i]
        plugin.logger.info(f"[COPY DEBUG] Processing arg[{i}]: '{arg}'")

        if arg == "-a" or arg == "--air":
            include_air = True
            plugin.logger.info(f"[COPY DEBUG] Include air enabled")
        elif arg == "-e" or arg == "--entities":
            copy_entities = True
            plugin.logger.info(f"[COPY DEBUG] Copy entities enabled")
        elif arg == "-b" or arg == "--biomes":
            copy_biomes = True
            plugin.logger.info(f"[COPY DEBUG] Copy biomes enabled")

        i += 1

    player_uuid = sender.unique_id
    pos1 = plugin.selections[player_uuid]['pos1']
    pos2 = plugin.selections[player_uuid]['pos2']

    dimension = sender.dimension
    player_location = sender.location

    min_x = min(pos1[0], pos2[0])
    max_x = max(pos1[0], pos2[0])
    min_y = min(pos1[1], pos2[1])
    max_y = max(pos1[1], pos2[1])
    min_z = min(pos1[2], pos2[2])
    max_z = max(pos1[2], pos2[2])

    blocks = []
    for x in range(int(min_x), int(max_x) + 1):
        for y in range(int(min_y), int(max_y) + 1):
            for z in range(int(min_z), int(max_z) + 1):
                block = dimension.get_block_at(x, y, z)

                # Skip air blocks unless include_air is True
                if not include_air and block.type == "minecraft:air":
                    continue

                relative_x = x - player_location.x
                relative_y = y - player_location.y
                relative_z = z - player_location.z
                blocks.append((relative_x, relative_y, relative_z, block.type, block.data))

    plugin.clipboard[player_uuid] = blocks

    # Build message
    msg = f"{len(blocks)} blocks copied"
    if include_air:
        msg += " (with air)"
    if copy_entities:
        msg += " (entities: not yet implemented)"
    if copy_biomes:
        msg += " (biomes: not yet implemented)"
    msg += "."

    sender.send_message(msg)
    plugin.logger.info(f"[COPY DEBUG] Copy completed: {len(blocks)} blocks")

    # Note: Container preservation is handled by /schem save instead
    # Regular copy/paste does not preserve containers (use schematics for that)

    return True
