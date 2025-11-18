from endstone_worldedit.utils import command_executor

command = {
    "smooth": {
        "description": "Smooths the terrain in the selection.",
        "usages": ["/smooth [iterations: int]"],
        "permissions": ["worldedit.command.smooth"]
    }
}

@command_executor("smooth", selection_required=True)
def handler(plugin, sender, args):
    """Smooth terrain in selection by averaging block heights.
    
    Args:
        plugin: Plugin instance
        sender: Command sender
        args: Command arguments (optional iterations)
    """
    player_uuid = sender.unique_id
    pos1 = plugin.selections[player_uuid]['pos1']
    pos2 = plugin.selections[player_uuid]['pos2']
    
    # Get iterations (aggressiveness)
    iterations = 1
    if len(args) > 0:
        try:
            iterations = int(args[0])
            if iterations < 1:
                iterations = 1
            elif iterations > 10:
                iterations = 10
        except ValueError:
            sender.send_message("§cIterations must be a number between 1 and 10§r")
            return False
    
    dimension = sender.dimension
    min_x = min(pos1[0], pos2[0])
    max_x = max(pos1[0], pos2[0])
    min_y = min(pos1[1], pos2[1])
    max_y = max(pos1[1], pos2[1])
    min_z = min(pos1[2], pos2[2])
    max_z = max(pos1[2], pos2[2])
    
    undo_entry = []
    plugin.redo_history[player_uuid] = []
    
    # Perform smoothing iterations
    for iteration in range(iterations):
        blocks_to_change = []
        
        # For each column in the selection
        for x in range(min_x, max_x + 1):
            for z in range(min_z, max_z + 1):
                # Find the top solid block in this column
                top_y = None
                for y in range(max_y, min_y - 1, -1):
                    block = dimension.get_block_at(x, y, z)
                    if block.type != "minecraft:air":
                        top_y = y
                        break
                
                if top_y is None:
                    continue
                
                # Calculate average height of neighbors
                neighbor_heights = []
                for dx in [-1, 0, 1]:
                    for dz in [-1, 0, 1]:
                        if dx == 0 and dz == 0:
                            continue
                        
                        nx, nz = x + dx, z + dz
                        if min_x <= nx <= max_x and min_z <= nz <= max_z:
                            # Find top block of neighbor
                            for ny in range(max_y, min_y - 1, -1):
                                neighbor_block = dimension.get_block_at(nx, ny, nz)
                                if neighbor_block.type != "minecraft:air":
                                    neighbor_heights.append(ny)
                                    break
                
                if not neighbor_heights:
                    continue
                
                # Calculate average height
                avg_height = sum(neighbor_heights) / len(neighbor_heights)
                target_y = int(avg_height)
                
                # Adjust this column towards average
                if top_y < target_y:
                    # Add blocks to raise terrain
                    current_block = dimension.get_block_at(x, top_y, z)
                    block_type = current_block.type
                    for y in range(top_y + 1, min(target_y + 1, max_y + 1)):
                        blocks_to_change.append((x, y, z, block_type, None))
                elif top_y > target_y:
                    # Remove blocks to lower terrain
                    for y in range(target_y + 1, min(top_y + 1, max_y + 1)):
                        blocks_to_change.append((x, y, z, "minecraft:air", None))
        
        # Apply changes
        for x, y, z, block_type, _ in blocks_to_change:
            block = dimension.get_block_at(x, y, z)
            if iteration == 0:  # Only save undo on first iteration
                undo_entry.append((x, y, z, block.type, block.data))
            block.set_type(block_type)
    
    # Save undo history
    if undo_entry:
        if player_uuid not in plugin.undo_history:
            plugin.undo_history[player_uuid] = []
        plugin.undo_history[player_uuid].append(undo_entry)
    
    affected = len(undo_entry)
    sender.send_message(f"§aTerrain smoothed with {iterations} iteration(s) ({affected} blocks affected)§r")
    return True

