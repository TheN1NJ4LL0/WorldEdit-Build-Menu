from endstone_worldedit.utils import command_executor

command = {
    "bmenu": {
        "description": "Opens the Builder's Menu for quick access to WorldEdit tools.",
        "usages": ["/bmenu"],
        "aliases": ["buildmenu", "bm"],
        "permissions": ["worldedit.builder.menu"]
    }
}

@command_executor("bmenu", area_check=False)
def handler(plugin, sender, args):
    """
    Display an interactive builder's menu with WorldEdit tools and area information
    """
    player_name = sender.name
    player_uuid = sender.unique_id
    world = sender.dimension.name
    location = sender.location
    is_op = sender.is_op
    
    area_manager = plugin.build_area_manager
    
    # Get player's build areas
    player_areas = area_manager.get_player_areas(player_name, world)
    current_areas = area_manager.get_areas_at_location(world, location.x, location.y, location.z)
    
    # Build the menu
    sender.send_message("§6╔════════════════════════════════════╗§r")
    sender.send_message("§6║      §e§lBUILDER'S MENU§r§6              ║§r")
    sender.send_message("§6╚════════════════════════════════════╝§r")
    sender.send_message("")
    
    # Current location status
    if is_op:
        sender.send_message("§a✓ §7Status: §eOperator §7(Can build anywhere)§r")
    elif current_areas:
        area_names = ", ".join([f"§e{area.name}§a" for area in current_areas])
        sender.send_message(f"§a✓ §7Status: §aIn build area ({area_names}§a)§r")
    else:
        sender.send_message("§c✗ §7Status: §cNot in a build area§r")
    
    sender.send_message("")
    sender.send_message("§6═══ Your Build Areas ═══§r")
    
    if player_areas:
        for area in player_areas[:5]:  # Show max 5 areas
            in_area = "§a●§r" if area in current_areas else "§7○§r"
            creative = "§eCreative§r" if area.creative_mode else "§7Survival§r"
            sender.send_message(f"  {in_area} §e{area.name}§7 - {creative} - {area.get_volume():,} blocks§r")
        
        if len(player_areas) > 5:
            sender.send_message(f"  §7... and {len(player_areas) - 5} more§r")
    else:
        sender.send_message("  §7No build areas assigned§r")
        if not is_op:
            sender.send_message("  §7Contact an admin to get build access§r")
    
    sender.send_message("")
    sender.send_message("§6═══ Quick Tools ═══§r")
    
    # Selection info
    if player_uuid in plugin.selections and 'pos1' in plugin.selections[player_uuid] and 'pos2' in plugin.selections[player_uuid]:
        pos1 = plugin.selections[player_uuid]['pos1']
        pos2 = plugin.selections[player_uuid]['pos2']
        
        # Calculate selection volume
        width = abs(pos2[0] - pos1[0]) + 1
        height = abs(pos2[1] - pos1[1]) + 1
        length = abs(pos2[2] - pos1[2]) + 1
        volume = width * height * length
        
        sender.send_message(f"  §a✓ Selection: §f{volume:,} blocks §7({width}×{height}×{length})§r")
    else:
        sender.send_message("  §7○ No selection - Use §e/wand§7 to get started§r")
    
    # Clipboard info
    if player_uuid in plugin.clipboard and plugin.clipboard[player_uuid]:
        clipboard_size = len(plugin.clipboard[player_uuid])
        sender.send_message(f"  §a✓ Clipboard: §f{clipboard_size:,} blocks§r")
    else:
        sender.send_message("  §7○ Clipboard empty§r")
    
    # Undo/Redo info
    undo_count = len(plugin.undo_history.get(player_uuid, []))
    redo_count = len(plugin.redo_history.get(player_uuid, []))
    sender.send_message(f"  §7History: §f{undo_count} undo§7, §f{redo_count} redo§r")
    
    sender.send_message("")
    sender.send_message("§6═══ Common Commands ═══§r")
    sender.send_message("  §e/wand§7 - Get selection tool§r")
    sender.send_message("  §e/set <block>§7 - Fill selection§r")
    sender.send_message("  §e/replace <from> <to>§7 - Replace blocks§r")
    sender.send_message("  §e/copy§7 - Copy selection§r")
    sender.send_message("  §e/paste§7 - Paste clipboard§r")
    sender.send_message("  §e/undo§7 - Undo last action§r")
    sender.send_message("  §e/schem save <name>§7 - Save schematic§r")
    sender.send_message("  §e/schem load <name>§7 - Load schematic§r")
    
    if player_areas:
        sender.send_message("")
        sender.send_message("§6═══ Area Commands ═══§r")
        sender.send_message("  §e/myareas§7 - List your build areas§r")
        sender.send_message("  §e/areainfo§7 - Info about current area§r")
    
    sender.send_message("")
    sender.send_message("§6════════════════════════════════════§r")
    
    return True

