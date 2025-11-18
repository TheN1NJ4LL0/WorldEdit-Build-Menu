"""Main plugin file for OnistoneBuilderLite."""

from pathlib import Path
from typing import Optional

from endstone.plugin import Plugin
from endstone.command import Command, CommandSender
from endstone.player import Player
from endstone.event import event_handler, PlayerInteractEvent, EventPriority

from .config import Config
from .permissions import Permissions
from .selection import SelectionManager, Position
from .clipboard import ClipboardManager
from .blueprints import BlueprintManager
from .zones import ZoneManager
from .undo import UndoManager
from .paste import PasteExecutor, PasteOptions, PasteOperation
from .menu import MenuHandler


class OnistoneBuilderLite(Plugin):
    """Main plugin class for OnistoneBuilderLite."""

    api_version = "0.5"

    def on_load(self) -> None:
        """Called when plugin is loaded."""
        self.logger.info("Loading OnistoneBuilderLite...")

        # Initialize configuration
        config_path = Path(self.data_folder) / "config.toml"
        self.config = Config(str(config_path))

        # Initialize managers
        self.selection_manager = SelectionManager()

        clipboard_limit = self.config.get("limits", "clipboardLimit", 10)
        self.clipboard_manager = ClipboardManager(max_size=clipboard_limit)

        blueprint_folder = self.config.get("paths", "blueprintFolder", "plugins/OnistoneBuilder/blueprints")
        shared_folder = self.config.get("paths", "sharedFolder", "plugins/OnistoneBuilder/blueprints/shared")
        self.blueprint_manager = BlueprintManager(blueprint_folder, shared_folder)

        self.zone_manager = ZoneManager()

        undo_depth = self.config.get("limits", "undoDepth", 5)
        self.undo_manager = UndoManager(max_depth=undo_depth)

        batch_size = self.config.get("performance", "batchSize", 4096)
        self.paste_executor = PasteExecutor(batch_size=batch_size)

        # Initialize menu handler
        self.menu_handler = MenuHandler(self)

        # Wand tracking
        self.wand_users: set[str] = set()

        self.logger.info("OnistoneBuilderLite loaded successfully!")

    def on_enable(self) -> None:
        """Called when plugin is enabled."""
        self.logger.info("Enabling OnistoneBuilderLite...")

        # Register commands
        self.register_commands()

        # Start zone cleanup task
        self.server.scheduler.run_task(
            self,
            self._cleanup_zones_task,
            delay=20 * 60,  # Every minute
            period=20 * 60
        )

        self.logger.info("OnistoneBuilderLite enabled!")

    def on_disable(self) -> None:
        """Called when plugin is disabled."""
        self.logger.info("OnistoneBuilderLite disabled!")

    def register_commands(self) -> None:
        """Register plugin commands."""
        # Main command is registered via plugin.yml
        pass

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        """Handle commands.

        Args:
            sender: Command sender
            command: Command object
            args: Command arguments

        Returns:
            True if command was handled
        """
        if command.name != "builder":
            return False

        if not isinstance(sender, Player):
            sender.send_message("§cThis command can only be used by players§r")
            return True

        player: Player = sender

        # No args = open menu
        if not args:
            self.menu_handler.show_main_menu(player)
            return True

        subcommand = args[0].lower()

        if subcommand == "wand":
            return self._handle_wand_command(player)
        elif subcommand == "pos1":
            return self._handle_pos1_command(player)
        elif subcommand == "pos2":
            return self._handle_pos2_command(player)
        elif subcommand == "undo":
            return self._handle_undo_command(player)
        elif subcommand == "zone":
            return self._handle_zone_command(player, args[1:])
        elif subcommand == "promote":
            return self._handle_promote_command(player, args[1:])
        else:
            player.send_message("§cUnknown subcommand. Use /builder for menu§r")
            return True

    def _handle_wand_command(self, player: Player) -> bool:
        """Handle /builder wand command.

        Args:
            player: Player executing command

        Returns:
            True if handled
        """
        if not Permissions.has_permission(player, Permissions.SELECT):
            player.send_message(Permissions.format_permission_error(Permissions.SELECT))
            return True

        player_uuid = player.unique_id

        if player_uuid in self.wand_users:
            self.wand_users.remove(player_uuid)
            player.send_message("§7Wand mode disabled§r")
        else:
            self.wand_users.add(player_uuid)
            player.send_message("§aWand mode enabled! Left-click = pos1, Right-click = pos2§r")


    def _handle_pos2_command(self, player: Player) -> bool:
        """Handle /builder pos2 command.

        Args:
            player: Player executing command

        Returns:
            True if handled
        """
        if not Permissions.has_permission(player, Permissions.SELECT):
            player.send_message(Permissions.format_permission_error(Permissions.SELECT))
            return True

        location = player.location
        pos = Position.from_location(location)
        dimension = player.dimension.name

        selection = self.selection_manager.get_selection(player.unique_id)
        selection.set_pos2(pos, dimension)

        player.send_message(f"§aPosition 2 set to ({pos.x}, {pos.y}, {pos.z})§r")

        if selection.is_complete():
            player.send_message(f"§7Selection: {selection}§r")

        return True

    def _handle_undo_command(self, player: Player) -> bool:
        """Handle /builder undo command.

        Args:
            player: Player executing command

        Returns:
            True if handled
        """
        if not self.undo_manager.can_undo(player.unique_id):
            player.send_message("§cNothing to undo§r")
            return True

        dimension = player.dimension
        entry = self.undo_manager.undo(player.unique_id, dimension)

        if entry:
            player.send_message(f"§aUndone: {entry.description} ({entry.get_block_count()} blocks)§r")
        else:
            player.send_message("§cUndo failed§r")

        return True

    def _handle_zone_command(self, player: Player, args: list[str]) -> bool:
        """Handle /builder zone command.

        Args:
            player: Player executing command
            args: Subcommand arguments

        Returns:
            True if handled
        """
        if not Permissions.has_permission(player, Permissions.ZONE):
            player.send_message(Permissions.format_permission_error(Permissions.ZONE))
            return True

        if not args or args[0].lower() != "here":
            player.send_message("§cUsage: /builder zone here <radius> [hours]§r")
            return True

        if len(args) < 2:
            player.send_message("§cUsage: /builder zone here <radius> [hours]§r")
            return True

        try:
            radius = int(args[1])
            duration = float(args[2]) if len(args) > 2 else self.config.get("zones", "defaultDurationHours", 12)
        except ValueError:
            player.send_message("§cInvalid radius or duration§r")
            return True

        location = player.location
        center = Position.from_location(location)
        dimension = player.dimension.name

        zone_name = f"{player.name}_zone_{len(self.zone_manager.zones) + 1}"

        zone = self.zone_manager.create_zone_at_location(
            zone_name,
            player.name,
            center,
            dimension,
            radius,
            duration
        )

        player.send_message(f"§aCreated builder zone '{zone_name}' (radius: {radius}, duration: {duration}h)§r")

        return True

    def _handle_promote_command(self, player: Player, args: list[str]) -> bool:
        """Handle /builder promote command.

        Args:
            player: Player executing command
            args: Command arguments

        Returns:
            True if handled
        """
        if not Permissions.has_permission(player, Permissions.ADMIN):
            player.send_message(Permissions.format_permission_error(Permissions.ADMIN))
            return True

        if not args:
            player.send_message("§cUsage: /builder promote <player>§r")
            return True

        target_name = args[0]
        player.send_message(f"§7Promotion system not yet implemented for {target_name}§r")

        return True

    def _cleanup_zones_task(self) -> None:
        """Background task to clean up expired zones."""
        removed = self.zone_manager.purge_expired()
        if removed > 0:
            self.logger.info(f"Cleaned up {removed} expired builder zones")

    @event_handler(priority=EventPriority.NORMAL)
    def on_player_interact(self, event: PlayerInteractEvent) -> None:
        """Handle player interact events for wand.

        Args:
            event: Player interact event
        """
        player = event.player

        if player.unique_id not in self.wand_users:
            return

        # Check if player is holding a wooden axe (wand)
        # Note: Endstone API may not have item checking yet, so this is a placeholder
        # In a real implementation, you'd check the item in hand

        block = event.block
        if block is None:
            return

        location = block.location
        pos = Position(int(location.x), int(location.y), int(location.z))
        dimension = player.dimension.name

        selection = self.selection_manager.get_selection(player.unique_id)

        # Left-click = pos1, Right-click = pos2
        # Note: Endstone API may not distinguish click types yet
        # This is a simplified implementation
        if not selection.pos1:
            selection.set_pos1(pos, dimension)
            player.send_message(f"§aPosition 1 set to ({pos.x}, {pos.y}, {pos.z})§r")
        else:
            selection.set_pos2(pos, dimension)
            player.send_message(f"§aPosition 2 set to ({pos.x}, {pos.y}, {pos.z})§r")

            if selection.is_complete():
                player.send_message(f"§7Selection: {selection}§r")

        event.cancelled = True
        """Handle /builder pos1 command.

        Args:
            player: Player executing command

        Returns:
            True if handled
        """
        if not Permissions.has_permission(player, Permissions.SELECT):
            player.send_message(Permissions.format_permission_error(Permissions.SELECT))
            return True

        location = player.location
        pos = Position.from_location(location)
        dimension = player.dimension.name

        selection = self.selection_manager.get_selection(player.unique_id)
        selection.set_pos1(pos, dimension)

        player.send_message(f"§aPosition 1 set to ({pos.x}, {pos.y}, {pos.z})§r")

        if selection.is_complete():
            player.send_message(f"§7Selection: {selection}§r")

        return True

