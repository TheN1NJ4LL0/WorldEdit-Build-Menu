"""Blueprint management commands for WorldEdit."""
from endstone_worldedit.utils import command_executor

command = {
    "blueprint": {
        "description": "Manage blueprints (personal clipboard saves).",
        "usages": [
            "/blueprint save <name>",
            "/blueprint load <name>",
            "/blueprint list",
            "/blueprint delete <name>",
            "/blueprint shared list",
            "/blueprint shared load <name>"
        ],
        "aliases": ["bp"],
        "permissions": ["worldedit.command.blueprint"]
    }
}

@command_executor("blueprint", area_check=False)
def handler(plugin, sender, args):
    """Handle blueprint commands.
    
    Args:
        plugin: Plugin instance
        sender: Command sender
        args: Command arguments
        
    Returns:
        True if command was handled
    """
    if len(args) < 1:
        sender.send_message("§cUsage: /blueprint <save|load|list|delete|shared> [name]§r")
        return False

    sub_command = args[0].lower()
    player_uuid = str(sender.unique_id)
    player_name = sender.name

    if sub_command == "save":
        if len(args) < 2:
            sender.send_message("§cUsage: /blueprint save <name>§r")
            return False

        name = args[1]

        # Check if player has clipboard
        if player_uuid not in plugin.clipboard or not plugin.clipboard[player_uuid]:
            sender.send_message("§cClipboard is empty! Use /copy first.§r")
            return False

        # Save blueprint
        clipboard_data = plugin.clipboard[player_uuid]
        success = plugin.blueprint_manager.save_blueprint(
            player_uuid,
            name,
            clipboard_data,
            author=player_name,
            shared=False
        )

        if success:
            sender.send_message(f"§aBlueprint '{name}' saved!§r")
            sender.send_message(f"§7Use /blueprint load {name} to load it§r")
        else:
            sender.send_message(f"§cFailed to save blueprint '{name}'§r")

        return True

    elif sub_command == "load":
        if len(args) < 2:
            sender.send_message("§cUsage: /blueprint load <name>§r")
            return False

        name = args[1]

        # Load blueprint
        blueprint = plugin.blueprint_manager.load_blueprint(player_uuid, name, from_shared=False)

        if blueprint is None:
            sender.send_message(f"§cBlueprint '{name}' not found!§r")
            sender.send_message(f"§7Use /blueprint list to see available blueprints§r")
            return False

        # Load into clipboard
        plugin.clipboard[player_uuid] = blueprint.clipboard_data

        sender.send_message(f"§aBlueprint '{name}' loaded into clipboard!§r")
        sender.send_message(f"§7Author: {blueprint.author}§r")
        sender.send_message(f"§7Use /paste to place it§r")

        return True

    elif sub_command == "list":
        blueprints = plugin.blueprint_manager.list_blueprints(player_uuid, include_shared=False)

        if not blueprints:
            sender.send_message("§7You don't have any saved blueprints.§r")
            sender.send_message("§7Use /blueprint save <name> to save your clipboard§r")
            return True

        sender.send_message(f"§6Your Blueprints §7({len(blueprints)} total)§6:§r")
        for bp_name in blueprints:
            sender.send_message(f"  §e- {bp_name}§r")
        sender.send_message(f"§7Use /blueprint load <name> to load a blueprint§r")

        return True

    elif sub_command == "delete":
        if len(args) < 2:
            sender.send_message("§cUsage: /blueprint delete <name>§r")
            return False

        name = args[1]

        # Delete blueprint
        success = plugin.blueprint_manager.delete_blueprint(player_uuid, name, from_shared=False)

        if success:
            sender.send_message(f"§aBlueprint '{name}' deleted!§r")
        else:
            sender.send_message(f"§cBlueprint '{name}' not found!§r")

        return True

    elif sub_command == "shared":
        if len(args) < 2:
            sender.send_message("§cUsage: /blueprint shared <list|load> [name]§r")
            return False

        shared_sub = args[1].lower()

        if shared_sub == "list":
            blueprints = plugin.blueprint_manager.list_blueprints(player_uuid, include_shared=True)
            shared_blueprints = [bp for bp in blueprints if bp.startswith("[Shared]")]

            if not shared_blueprints:
                sender.send_message("§7No shared blueprints available.§r")
                return True

            sender.send_message(f"§6Shared Blueprints §7({len(shared_blueprints)} total)§6:§r")
            for bp_name in shared_blueprints:
                clean_name = bp_name.replace("[Shared] ", "")
                sender.send_message(f"  §e- {clean_name}§r")
            sender.send_message(f"§7Use /blueprint shared load <name> to load§r")

            return True

        elif shared_sub == "load":
            if len(args) < 3:
                sender.send_message("§cUsage: /blueprint shared load <name>§r")
                return False

            name = args[2]

            # Load shared blueprint
            blueprint = plugin.blueprint_manager.load_blueprint(player_uuid, name, from_shared=True)

            if blueprint is None:
                sender.send_message(f"§cShared blueprint '{name}' not found!§r")
                return False

            # Load into clipboard
            plugin.clipboard[player_uuid] = blueprint.clipboard_data

            sender.send_message(f"§aShared blueprint '{name}' loaded!§r")
            sender.send_message(f"§7Author: {blueprint.author}§r")
            sender.send_message(f"§7Use /paste to place it§r")

            return True

    sender.send_message(f"§cUnknown sub-command '{sub_command}'§r")
    sender.send_message("§7Use: save, load, list, delete, or shared§r")
    return False

