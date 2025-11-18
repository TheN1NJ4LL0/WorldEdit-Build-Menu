"""Builder menu command for WorldEdit."""

command = {
    "builder": {
        "description": "Open the builder menu",
        "usage": "/builder - Open builder menu",
        "aliases": ["b", "buildermenu"],
        "permission": None
    }
}


def handler(plugin, sender, args):
    """Handle the builder command.

    Args:
        plugin: Plugin instance
        sender: Command sender
        args: Command arguments

    Returns:
        True if command was handled
    """
    from endstone import Player

    if not isinstance(sender, Player):
        sender.send_message("§cThis command can only be used by players§r")
        return True

    player = sender

    # Open builder menu
    if plugin.menu_handler:
        plugin.menu_handler.show_main_menu(player)
    else:
        player.send_message("§cBuilder menu is not available§r")

    return True

