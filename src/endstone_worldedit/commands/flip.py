from endstone_worldedit.utils import command_executor

command = {
    "flip": {
        "description": "Flips the selection along an axis.",
        "usages": ["/flip [x|y|z]"],
        "permissions": ["worldedit.command.flip"]
    }
}

@command_executor("flip", selection_required=True)
def handler(plugin, sender, args):
    """Flip the selection along an axis.
    
    Args:
        plugin: WorldEdit plugin instance
        sender: Player executing the command
        args: Command arguments [axis]
    """
    # Default to player's facing direction if no axis specified
    axis = "z"  # Default
    if len(args) > 0:
        axis = args[0].lower()
        if axis not in ["x", "y", "z"]:
            sender.send_message("§cUsage: /flip [x|y|z]§r")
            sender.send_message("§7x = left/right, y = up/down, z = forward/backward§r")
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
    
    # Flip and place blocks
    blocks_to_place = []
    for rel_x, rel_y, rel_z, block_type, data_value in blocks:
        # Apply flip
        if axis == "x":
            # Flip along X axis (left/right)
            new_rel_x = width - 1 - rel_x
            new_rel_y = rel_y
            new_rel_z = rel_z
        elif axis == "y":
            # Flip along Y axis (up/down)
            new_rel_x = rel_x
            new_rel_y = height - 1 - rel_y
            new_rel_z = rel_z
        elif axis == "z":
            # Flip along Z axis (forward/backward)
            new_rel_x = rel_x
            new_rel_y = rel_y
            new_rel_z = length - 1 - rel_z
        else:
            new_rel_x = rel_x
            new_rel_y = rel_y
            new_rel_z = rel_z
        
        # Convert back to world coordinates
        world_x = int(min_x + new_rel_x)
        world_y = int(min_y + new_rel_y)
        world_z = int(min_z + new_rel_z)
        
        blocks_to_place.append((world_x, world_y, world_z, block_type, data_value))
    
    # Place flipped blocks
    affected_blocks = len(blocks_to_place)
    
    if affected_blocks > plugin.plugin_config["async-threshold"]:
        plugin.tasks[player_uuid] = {"dimension": dimension, "blocks": blocks_to_place}
        sender.send_message(f"§aFlipping {affected_blocks} blocks along {axis.upper()}-axis (async)...§r")
    else:
        for x, y, z, block_type, data_value in blocks_to_place:
            block = dimension.get_block_at(x, y, z)
            block.set_type(block_type)
            if data_value is not None:
                block.set_data(data_value)
        sender.send_message(f"§aFlipped {affected_blocks} blocks along {axis.upper()}-axis§r")
    
    return True

