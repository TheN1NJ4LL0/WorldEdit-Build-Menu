"""
Utility functions for working with Minecraft Bedrock structure files (.mcstructure).
Uses the /structure save and /structure load commands to preserve block entities (containers).
"""

import os
from pathlib import Path


def structure_save(plugin, player, structure_name, pos1, pos2, include_entities=True, include_blocks=True):
    """
    Save a structure using the /structure save command.
    This preserves block entities (chests, furnaces, etc.) and entities.
    
    Args:
        plugin: The plugin instance
        player: The player executing the command
        structure_name: Name to save the structure as
        pos1: Tuple of (x, y, z) for first corner
        pos2: Tuple of (x, y, z) for second corner
        include_entities: Whether to include entities (default: True)
        include_blocks: Whether to include blocks (default: True)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert to integers to avoid float issues
        x1, y1, z1 = int(pos1[0]), int(pos1[1]), int(pos1[2])
        x2, y2, z2 = int(pos2[0]), int(pos2[1]), int(pos2[2])

        # Build the command
        # /structure save <name> <from: x y z> <to: x y z> [saveMode] [includesEntities] [includesBlocks]
        # Note: The optional parameters must ALL be provided or NONE
        # If we provide saveMode, we MUST provide includesEntities and includesBlocks

        # Simple version without optional parameters (uses defaults: disk, true, true)
        cmd = f"structure save {structure_name} {x1} {y1} {z1} {x2} {y2} {z2}"

        plugin.logger.info(f"[STRUCTURE SAVE] Executing: {cmd}")

        # Execute the command as the player
        player.perform_command(cmd)

        plugin.logger.info(f"[STRUCTURE SAVE] Successfully saved structure: {structure_name}")
        return True

    except Exception as e:
        plugin.logger.error(f"[STRUCTURE SAVE] Error saving structure {structure_name}: {e}")
        return False


def structure_load(plugin, player, structure_name, location, rotation=0, mirror="none", 
                   animation_mode="all_at_once", animation_seconds=0.0,
                   include_entities=True, include_blocks=True):
    """
    Load a structure using the /structure load command.
    This restores block entities (chests, furnaces, etc.) and entities.
    
    Args:
        plugin: The plugin instance
        player: The player executing the command
        structure_name: Name of the structure to load
        location: Tuple of (x, y, z) where to load the structure
        rotation: Rotation in degrees (0, 90, 180, 270)
        mirror: Mirror mode ("none", "x", "z", "xz")
        animation_mode: How to animate ("all_at_once", "layer_by_layer", "block_by_block")
        animation_seconds: How long the animation takes (0.0 for instant)
        include_entities: Whether to include entities (default: True)
        include_blocks: Whether to include blocks (default: True)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert to integers to avoid float issues
        x, y, z = int(location[0]), int(location[1]), int(location[2])

        # Convert rotation to Bedrock format
        rotation_map = {
            0: "0_degrees",
            90: "90_degrees",
            180: "180_degrees",
            270: "270_degrees"
        }
        rotation_str = rotation_map.get(rotation, "0_degrees")

        # Build the command
        # /structure load <name> <to: x y z> [rotation] [mirror] [animationMode] [animationSeconds]
        # Note: Optional parameters - if we want default behavior, use minimal command

        # Check if we need transformations
        if rotation == 0 and mirror == "none":
            # Simple version without transformations
            cmd = f"structure load {structure_name} {x} {y} {z}"
        else:
            # Version with transformations (rotation and/or mirror)
            cmd = f"structure load {structure_name} {x} {y} {z} {rotation_str} {mirror}"

        plugin.logger.info(f"[STRUCTURE LOAD] Executing: {cmd}")

        # Execute the command as the player
        player.perform_command(cmd)

        plugin.logger.info(f"[STRUCTURE LOAD] Successfully loaded structure: {structure_name}")
        return True

    except Exception as e:
        plugin.logger.error(f"[STRUCTURE LOAD] Error loading structure {structure_name}: {e}")
        return False


def structure_exists(plugin, structure_name):
    """
    Check if a structure file exists.

    Since we can't easily access the world folder from Endstone,
    we'll always return True and let the structure load command fail gracefully.

    Args:
        plugin: The plugin instance
        structure_name: Name of the structure

    Returns:
        True (always assumes structure might exist)
    """
    # We can't easily check file existence without access to world folder
    # The structure load command will fail gracefully if it doesn't exist
    # So we return True to attempt loading, and handle failure in structure_load
    plugin.logger.info(f"[STRUCTURE EXISTS] Assuming structure '{structure_name}' might exist")
    return True


def structure_delete(plugin, player, structure_name):
    """
    Delete a structure using the /structure delete command.
    
    Args:
        plugin: The plugin instance
        player: The player executing the command
        structure_name: Name of the structure to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        cmd = f"structure delete {structure_name}"
        plugin.logger.info(f"[STRUCTURE DELETE] Executing: {cmd}")
        player.perform_command(cmd)
        plugin.logger.info(f"[STRUCTURE DELETE] Successfully deleted structure: {structure_name}")
        return True
    except Exception as e:
        plugin.logger.error(f"[STRUCTURE DELETE] Error deleting structure {structure_name}: {e}")
        return False

