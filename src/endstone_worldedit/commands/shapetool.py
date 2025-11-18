from endstone.inventory import ItemStack
from endstone_worldedit.utils import command_executor

command = {
    "shapetool": {
        "description": "Gives the user the shape tool (wooden shovel).",
        "usage": "/shapetool",
        "aliases": ["sht"],
        "permissions": ["worldedit.command.shapetool"]
    }
}

@command_executor("shapetool", area_check=False)
def handler(plugin, sender, args):
    sender.inventory.add_item(ItemStack("minecraft:wooden_shovel"))
    sender.send_message("§6You have been given the shape tool!")
    sender.send_message("§7Sneak + Right-click to configure shapes")
    sender.send_message("§7Right-click to spawn configured shapes§r")
    return True



