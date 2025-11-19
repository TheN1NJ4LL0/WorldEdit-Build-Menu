from endstone_worldedit.utils import command_executor

command = {
    "hpyramid": {
        "description": "Creates a hollow pyramid.",
        "permissions": ["worldedit.command.pyramid"]
    }
}

@command_executor("hpyramid")
def handler(plugin, sender, args):
    if len(args) < 2:
        sender.send_message("Usage: /hpyramid <block> <size>")
        return False

    block_name = args[0]
    try:
        size = int(args[1])
    except ValueError:
        sender.send_message("Size must be an integer.")
        return False

    player_uuid = sender.unique_id
    dimension = sender.dimension
    center = sender.location

    undo_entry = []
    plugin.redo_history[player_uuid] = []

    blocks_to_change = []
    
    # Build hollow pyramid from bottom to top
    for level in range(size):
        y = int(center.y) + level
        current_size = size - level
        
        # Create a hollow square layer at this level (only edges)
        for x in range(int(center.x) - current_size, int(center.x) + current_size + 1):
            for z in range(int(center.z) - current_size, int(center.z) + current_size + 1):
                # Only place blocks on the edges
                if (x == int(center.x) - current_size or 
                    x == int(center.x) + current_size or 
                    z == int(center.z) - current_size or 
                    z == int(center.z) + current_size):
                    blocks_to_change.append((x, y, z, block_name, None))

    affected_blocks = len(blocks_to_change)

    for x, y, z, _, _ in blocks_to_change:
        block = dimension.get_block_at(x, y, z)
        undo_entry.append((x, y, z, block.type, block.data))

    if player_uuid not in plugin.undo_history:
        plugin.undo_history[player_uuid] = []
    plugin.undo_history[player_uuid].append(undo_entry)

    if affected_blocks > plugin.plugin_config["async-threshold"]:
        plugin.tasks[player_uuid] = {"dimension": dimension, "blocks": blocks_to_change}
        sender.send_message(f"Starting async operation for {affected_blocks} blocks...")
    else:
        for x, y, z, block_type, data_value in blocks_to_change:
            block = dimension.get_block_at(x, y, z)
            block.set_type(block_type)
            if data_value is not None:
                block.set_data(data_value)
        sender.send_message(f"Hollow pyramid created ({affected_blocks} blocks affected).")
        
    return True

