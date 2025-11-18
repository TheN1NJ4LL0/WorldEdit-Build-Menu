from endstone_worldedit.utils import command_executor

command = {
    "areainfo": {
        "description": "Shows information about the build area you're currently in.",
        "usages": ["/areainfo"],
        "permissions": ["worldedit.builder.menu"]
    }
}

@command_executor("areainfo", area_check=False)
def handler(plugin, sender, args):
    """Show information about the current build area"""
    player_name = sender.name
    world = sender.dimension.name
    location = sender.location
    area_manager = plugin.build_area_manager
    
    # Get areas at current location
    current_areas = area_manager.get_areas_at_location(world, location.x, location.y, location.z)
    
    if not current_areas:
        sender.send_message("§7You are not currently in a build area.§r")
        
        # Show nearby areas if player has any
        player_areas = area_manager.get_player_areas(player_name, world)
        if player_areas:
            sender.send_message("")
            sender.send_message("§7Your build areas in this world:§r")
            for area in player_areas[:3]:
                sender.send_message(f"  §e{area.name}§7 - Use §e/area tp {area.name}§r")
        return True
    
    sender.send_message("§6Current Build Area Information:§r")
    sender.send_message("")
    
    for area in current_areas:
        # Check if player has access
        has_access = sender.is_op or area.has_builder(player_name)
        access_status = "§a✓ Authorized§r" if has_access else "§c✗ Not Authorized§r"
        
        sender.send_message(f"§6Area: §e{area.name}§r")
        sender.send_message(f"§7World: §f{area.world}§r")
        sender.send_message(f"§7Access: {access_status}§r")
        sender.send_message(f"§7Creative Mode: §f{'Enabled' if area.creative_mode else 'Disabled'}§r")
        sender.send_message(f"§7Volume: §f{area.get_volume():,} blocks§r")
        sender.send_message(f"§7Bounds:§r")
        sender.send_message(f"  §7X: §f{area.min_x} §7to §f{area.max_x}§r")
        sender.send_message(f"  §7Y: §f{area.min_y} §7to §f{area.max_y}§r")
        sender.send_message(f"  §7Z: §f{area.min_z} §7to §f{area.max_z}§r")
        
        if has_access:
            sender.send_message("")
            sender.send_message("§aYou can use WorldEdit commands in this area!§r")
        else:
            sender.send_message("")
            sender.send_message("§cYou need permission to build here.§r")
        
        sender.send_message("")
    
    return True

