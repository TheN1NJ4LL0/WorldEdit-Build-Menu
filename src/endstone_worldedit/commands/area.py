from endstone_worldedit.utils import command_executor

command = {
    "area": {
        "description": "Manages build areas for builders.",
        "usages": [
            "/area create <name: string>",
            "/area delete <name: string>",
            "/area list",
            "/area info <name: string>",
            "/area addbuilder <area: string> <player: string>",
            "/area removebuilder <area: string> <player: string>",
            "/area tp <name: string>"
        ],
        "permissions": ["worldedit.admin.area"]
    }
}

@command_executor("area", area_check=False)
def handler(plugin, sender, args):
    if len(args) < 1:
        sender.send_message("§cUsage: /area <create|delete|list|info|addbuilder|removebuilder|tp> [args]§r")
        return False
    
    sub_command = args[0].lower()
    area_manager = plugin.build_area_manager
    
    if sub_command == "create":
        if len(args) < 2:
            sender.send_message("§cUsage: /area create <name>§r")
            return False
        
        name = args[1]
        player_uuid = sender.unique_id
        
        # Check if player has a selection
        if player_uuid not in plugin.selections or 'pos1' not in plugin.selections[player_uuid] or 'pos2' not in plugin.selections[player_uuid]:
            sender.send_message("§cYou must set both positions first using the wand or /pos1 and /pos2.§r")
            return False
        
        pos1 = plugin.selections[player_uuid]['pos1']
        pos2 = plugin.selections[player_uuid]['pos2']
        world = sender.dimension.name
        
        # Create the area
        if area_manager.create_area(name, world, pos1, pos2):
            sender.send_message(f"§aCreated build area '§e{name}§a' in world '§e{world}§a'.§r")
            sender.send_message(f"§7Use /area addbuilder {name} <player> to add builders.§r")
            return True
        else:
            sender.send_message(f"§cBuild area '§e{name}§c' already exists.§r")
            return False
    
    elif sub_command == "delete":
        if len(args) < 2:
            sender.send_message("§cUsage: /area delete <name>§r")
            return False
        
        name = args[1]
        if area_manager.delete_area(name):
            sender.send_message(f"§aDeleted build area '§e{name}§a'.§r")
            return True
        else:
            sender.send_message(f"§cBuild area '§e{name}§c' not found.§r")
            return False
    
    elif sub_command == "list":
        world = sender.dimension.name if len(args) < 2 else args[1]
        areas = area_manager.list_areas(world)
        
        if not areas:
            sender.send_message(f"§7No build areas found in world '§e{world}§7'.§r")
            return True
        
        sender.send_message(f"§6Build Areas in '§e{world}§6':§r")
        for area in areas:
            builder_count = len(area.builders)
            sender.send_message(f"  §e{area.name}§7 - {builder_count} builder(s), {area.get_volume():,} blocks§r")
        return True
    
    elif sub_command == "info":
        if len(args) < 2:
            sender.send_message("§cUsage: /area info <name>§r")
            return False
        
        name = args[1]
        area = area_manager.get_area(name)
        
        if not area:
            sender.send_message(f"§cBuild area '§e{name}§c' not found.§r")
            return False
        
        sender.send_message(area.get_info())
        return True
    
    elif sub_command == "addbuilder":
        if len(args) < 3:
            sender.send_message("§cUsage: /area addbuilder <area> <player>§r")
            return False
        
        area_name = args[1]
        player_name = args[2]
        
        if area_manager.add_builder_to_area(area_name, player_name):
            sender.send_message(f"§aAdded '§e{player_name}§a' as a builder to area '§e{area_name}§a'.§r")
            return True
        else:
            sender.send_message(f"§cBuild area '§e{area_name}§c' not found.§r")
            return False
    
    elif sub_command == "removebuilder":
        if len(args) < 3:
            sender.send_message("§cUsage: /area removebuilder <area> <player>§r")
            return False
        
        area_name = args[1]
        player_name = args[2]
        
        if area_manager.remove_builder_from_area(area_name, player_name):
            sender.send_message(f"§aRemoved '§e{player_name}§a' from build area '§e{area_name}§a'.§r")
            return True
        else:
            sender.send_message(f"§cBuild area '§e{area_name}§c' not found.§r")
            return False
    
    elif sub_command == "tp":
        if len(args) < 2:
            sender.send_message("§cUsage: /area tp <name>§r")
            return False
        
        name = args[1]
        area = area_manager.get_area(name)
        
        if not area:
            sender.send_message(f"§cBuild area '§e{name}§c' not found.§r")
            return False
        
        # Teleport to center of area
        center_x = (area.min_x + area.max_x) / 2
        center_y = area.min_y
        center_z = (area.min_z + area.max_z) / 2
        
        sender.send_message(f"§aTeleporting to build area '§e{name}§a'...§r")
        sender.send_message(f"§7Center: ({center_x:.1f}, {center_y}, {center_z:.1f})§r")
        return True
    
    else:
        sender.send_message(f"§cUnknown sub-command '§e{sub_command}§c'.§r")
        return False

