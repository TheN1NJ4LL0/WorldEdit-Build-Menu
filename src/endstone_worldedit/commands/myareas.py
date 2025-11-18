from endstone_worldedit.utils import command_executor

command = {
    "myareas": {
        "description": "Lists all build areas you have access to.",
        "usages": ["/myareas"],
        "permissions": ["worldedit.builder.menu"]
    }
}

@command_executor("myareas", area_check=False)
def handler(plugin, sender, args):
    """List all build areas the player has access to"""
    player_name = sender.name
    area_manager = plugin.build_area_manager
    
    # Get all areas for this player
    all_areas = area_manager.get_player_areas(player_name)
    
    if not all_areas:
        sender.send_message("§7You don't have access to any build areas.§r")
        sender.send_message("§7Contact an admin to get build permissions.§r")
        return True
    
    sender.send_message(f"§6Your Build Areas §7({len(all_areas)} total)§6:§r")
    sender.send_message("")
    
    # Group by world
    areas_by_world = {}
    for area in all_areas:
        if area.world not in areas_by_world:
            areas_by_world[area.world] = []
        areas_by_world[area.world].append(area)
    
    # Display areas grouped by world
    for world, areas in areas_by_world.items():
        sender.send_message(f"§e{world}:§r")
        for area in areas:
            creative = "§aCreative§r" if area.creative_mode else "§7Survival§r"
            volume = area.get_volume()
            sender.send_message(f"  §6{area.name}§r")
            sender.send_message(f"    §7Mode: {creative}§r")
            sender.send_message(f"    §7Size: §f{volume:,} blocks§r")
            sender.send_message(f"    §7Pos1: §f({area.pos1[0]}, {area.pos1[1]}, {area.pos1[2]})§r")
            sender.send_message(f"    §7Pos2: §f({area.pos2[0]}, {area.pos2[1]}, {area.pos2[2]})§r")
        sender.send_message("")
    
    sender.send_message("§7Use §e/bmenu§7 to open the builder's menu§r")
    return True

