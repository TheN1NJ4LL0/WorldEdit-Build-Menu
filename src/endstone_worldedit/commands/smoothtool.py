from endstone.inventory import ItemStack
from endstone_worldedit.utils import command_executor

command = {
    "smoothtool": {
        "description": "Gives the user the smooth tool (wooden hoe).",
        "usage": "/smoothtool",
        "aliases": ["st"],
        "permissions": ["worldedit.command.smoothtool"]
    }
}

@command_executor("smoothtool", area_check=False)
def handler(plugin, sender, args):
    sender.inventory.add_item(ItemStack("minecraft:wooden_hoe"))
    sender.send_message("§6You have been given the smooth tool!")
    sender.send_message("§7Sneak + Right-click to configure smooth settings")
    sender.send_message("§7Right-click to apply smooth at your crosshair§r")
    return True

