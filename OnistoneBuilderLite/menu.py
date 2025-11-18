"""Menu handlers for OnistoneBuilderLite."""

from typing import TYPE_CHECKING, Optional
from server_ui import ActionForm, ModalForm, MessageForm

from .ui_components import UIBuilder
from .permissions import Permissions
from .paste import PasteOptions, Rotation

if TYPE_CHECKING:
    from endstone.player import Player
    from .main import OnistoneBuilderLite


class MenuHandler:
    """Handles UI menu interactions."""
    
    def __init__(self, plugin: "OnistoneBuilderLite"):
        """Initialize menu handler.
        
        Args:
            plugin: Plugin instance
        """
        self.plugin = plugin
    
    def show_main_menu(self, player: "Player") -> None:
        """Show main builder menu.
        
        Args:
            player: Player to show menu to
        """
        if not Permissions.has_permission(player, Permissions.MENU):
            player.send_message(Permissions.format_permission_error(Permissions.MENU))
            return
        
        form = UIBuilder.create_main_menu(player)
        
        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return
            
            if data == 0:  # Selection
                self.show_selection_menu(player)
            elif data == 1:  # Clipboard
                self.show_clipboard_menu(player)
            elif data == 2:  # Blueprints
                self.show_blueprint_menu(player)
            elif data == 3:  # Zones
                self.show_zone_menu(player)
            elif data == 4:  # Undo
                self.handle_undo(player)
            # data == 5 is Close, do nothing
        
        form.send(player, on_submit)
    
    def show_selection_menu(self, player: "Player") -> None:
        """Show selection menu.
        
        Args:
            player: Player to show menu to
        """
        selection = self.plugin.selection_manager.get_selection(player.unique_id)
        has_selection = selection.is_complete()
        
        if has_selection:
            info = f"§a{selection}§r"
        else:
            info = "§7No selection§r"
        
        form = UIBuilder.create_selection_menu(player, has_selection, info)
        
        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return
            
            if data == 0:  # Set pos1
                self.handle_set_pos1(player)
            elif data == 1:  # Set pos2
                self.handle_set_pos2(player)
            elif data == 2 and has_selection:  # Clear
                self.plugin.selection_manager.clear_selection(player.unique_id)
                player.send_message("§aSelection cleared§r")
            else:  # Back
                self.show_main_menu(player)
        
        form.send(player, on_submit)
    
    def show_clipboard_menu(self, player: "Player") -> None:
        """Show clipboard menu.
        
        Args:
            player: Player to show menu to
        """
        clipboard_count = self.plugin.clipboard_manager.get_count(player.unique_id)
        
        form = UIBuilder.create_clipboard_menu(player, clipboard_count)
        
        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return
            
            if data == 0:  # Copy
                self.handle_copy(player)
            elif data == 1:  # Cut
                self.handle_cut(player)
            elif data == 2:  # Paste
                self.show_paste_options(player)
            elif data == 3:  # Browse
                player.send_message("§7Clipboard browser not yet implemented§r")
            else:  # Back
                self.show_main_menu(player)
        
        form.send(player, on_submit)
    
    def show_paste_options(self, player: "Player") -> None:
        """Show paste options form.
        
        Args:
            player: Player to show menu to
        """
        form = UIBuilder.create_paste_options_form()
        
        def on_submit(player: "Player", data: Optional[list]):
            if data is None:
                return
            
            # Parse options
            options = PasteOptions()
            options.rotation = [Rotation.NONE, Rotation.ROTATE_90, Rotation.ROTATE_180, Rotation.ROTATE_270][data[0]]
            options.flip_x = data[1]
            options.flip_y = data[2]
            options.flip_z = data[3]
            options.offset_x = int(data[4])
            options.offset_y = int(data[5])
            options.offset_z = int(data[6])
            options.place_air = data[7]
            options.ignore_liquids = data[8]
            
            self.handle_paste(player, options)
        
        form.send(player, on_submit)
    
    def show_blueprint_menu(self, player: "Player") -> None:
        """Show blueprint menu.
        
        Args:
            player: Player to show menu to
        """
        blueprints = self.plugin.blueprint_manager.list_blueprints(player.unique_id)
        
        form = UIBuilder.create_blueprint_menu(player, blueprints)
        
        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return
            
            if data == 0:  # Save
                self.show_save_blueprint_form(player)
            elif data == 1:  # Load
                player.send_message("§7Blueprint loader not yet implemented§r")
            elif data == 2:  # Browse
                player.send_message("§7Blueprint browser not yet implemented§r")
            elif data == 3:  # Shared
                player.send_message("§7Shared blueprints not yet implemented§r")
            else:  # Back
                self.show_main_menu(player)
        
        form.send(player, on_submit)
    
    def show_save_blueprint_form(self, player: "Player") -> None:
        """Show save blueprint form.
        
        Args:
            player: Player to show menu to
        """
        form = UIBuilder.create_input_form("§l§2Save Blueprint§r", "Blueprint Name:", "my_build")
        
        def on_submit(player: "Player", data: Optional[list]):
            if data is None or not data[0]:
                return
            
            name = data[0].strip()
            self.handle_save_blueprint(player, name)
        
        form.send(player, on_submit)
    
    def show_zone_menu(self, player: "Player") -> None:
        """Show zone menu.
        
        Args:
            player: Player to show menu to
        """
        zones = self.plugin.zone_manager.get_player_zones(player.name)
        zone_names = [z.name for z in zones]
        
        form = UIBuilder.create_zone_menu(player, zone_names)
        
        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return
            
            if data == 0:  # Create zone
                self.show_create_zone_form(player)
            elif data == 1:  # My zones
                player.send_message("§7Zone browser not yet implemented§r")
            elif data == 2:  # Share
                player.send_message("§7Zone sharing not yet implemented§r")
            else:  # Back
                self.show_main_menu(player)
        
        form.send(player, on_submit)
    
    def show_create_zone_form(self, player: "Player") -> None:
        """Show create zone form.
        
        Args:
            player: Player to show menu to
        """
        form = ModalForm()
        form.title("§l§2Create Builder Zone§r")
        form.text_input("Zone Name:", placeholder="my_zone")
        form.slider("Radius:", 8, 64, step=8, default=32)
        form.slider("Duration (hours):", 1, 72, step=1, default=12)
        
        def on_submit(player: "Player", data: Optional[list]):
            if data is None or not data[0]:
                return
            
            name = data[0].strip()
            radius = int(data[1])
            duration = float(data[2])
            
            self.handle_create_zone(player, name, radius, duration)
        
        form.send(player, on_submit)
    
    # Handler methods
    def handle_set_pos1(self, player: "Player") -> None:
        """Handle set position 1."""
        from .selection import Position

        location = player.location
        pos = Position.from_location(location)
        dimension = player.dimension.name

        selection = self.plugin.selection_manager.get_selection(player.unique_id)
        selection.set_pos1(pos, dimension)

        player.send_message(f"§aPosition 1 set to ({pos.x}, {pos.y}, {pos.z})§r")

        if selection.is_complete():
            player.send_message(f"§7Selection: {selection}§r")

    def handle_set_pos2(self, player: "Player") -> None:
        """Handle set position 2."""
        from .selection import Position

        location = player.location
        pos = Position.from_location(location)
        dimension = player.dimension.name

        selection = self.plugin.selection_manager.get_selection(player.unique_id)
        selection.set_pos2(pos, dimension)

        player.send_message(f"§aPosition 2 set to ({pos.x}, {pos.y}, {pos.z})§r")

        if selection.is_complete():
            player.send_message(f"§7Selection: {selection}§r")

    def handle_copy(self, player: "Player") -> None:
        """Handle copy operation."""
        if not Permissions.has_permission(player, Permissions.COPY):
            player.send_message(Permissions.format_permission_error(Permissions.COPY))
            return

        selection = self.plugin.selection_manager.get_selection(player.unique_id)

        if not selection.is_complete():
            player.send_message("§cNo selection! Use /builder pos1 and /builder pos2§r")
            return

        # Check volume limit
        volume = selection.get_volume()
        max_volume = self.plugin.config.get("limits", "maxSelectionVolume", 250000)

        if volume > max_volume:
            player.send_message(f"§cSelection too large! Max: {max_volume} blocks§r")
            return

        # Copy region
        min_pos, max_pos = selection.get_bounds()
        dimension = player.dimension

        clipboard_entry = self.plugin.clipboard_manager.copy_region(
            dimension,
            min_pos,
            max_pos,
            min_pos,
            include_air=True
        )

        self.plugin.clipboard_manager.add_entry(player.unique_id, clipboard_entry)

        player.send_message(f"§aCopied {clipboard_entry.get_block_count()} blocks to clipboard§r")

    def handle_cut(self, player: "Player") -> None:
        """Handle cut operation."""
        if not Permissions.has_permission(player, Permissions.CUT):
            player.send_message(Permissions.format_permission_error(Permissions.CUT))
            return

        # First copy
        self.handle_copy(player)

        # Then replace with air
        selection = self.plugin.selection_manager.get_selection(player.unique_id)

        if not selection.is_complete():
            return

        min_pos, max_pos = selection.get_bounds()
        dimension = player.dimension

        count = 0
        for y in range(min_pos.y, max_pos.y + 1):
            for z in range(min_pos.z, max_pos.z + 1):
                for x in range(min_pos.x, max_pos.x + 1):
                    block = dimension.get_block_at(x, y, z)
                    block.set_type("minecraft:air")
                    count += 1

        player.send_message(f"§aCut {count} blocks§r")

    def handle_paste(self, player: "Player", options: PasteOptions) -> None:
        """Handle paste operation."""
        if not Permissions.has_permission(player, Permissions.PASTE):
            player.send_message(Permissions.format_permission_error(Permissions.PASTE))
            return

        clipboard_entry = self.plugin.clipboard_manager.get_latest(player.unique_id)

        if not clipboard_entry:
            player.send_message("§cClipboard is empty!§r")
            return

        from .paste import PasteOperation
        from .selection import Position

        operation = PasteOperation(clipboard_entry, options)

        # Check volume limit
        volume = operation.get_affected_volume()
        max_volume = self.plugin.config.get("limits", "maxPasteVolume", 100000)

        if volume > max_volume:
            player.send_message(f"§cPaste too large! Max: {max_volume} blocks§r")
            return

        # Get target position
        location = player.location
        target = Position.from_location(location)

        # Execute paste
        dimension = player.dimension

        player.send_message("§7Pasting...§r")

        # Note: This should be async in a real implementation
        import asyncio
        placed = asyncio.run(self.plugin.paste_executor.execute_paste(
            dimension,
            operation,
            target,
            player
        ))

        player.send_message(f"§aPasted {placed} blocks§r")

    def handle_undo(self, player: "Player") -> None:
        """Handle undo operation."""
        if not self.plugin.undo_manager.can_undo(player.unique_id):
            player.send_message("§cNothing to undo§r")
            return

        dimension = player.dimension
        entry = self.plugin.undo_manager.undo(player.unique_id, dimension)

        if entry:
            player.send_message(f"§aUndone: {entry.description} ({entry.get_block_count()} blocks)§r")
        else:
            player.send_message("§cUndo failed§r")

    def handle_save_blueprint(self, player: "Player", name: str) -> None:
        """Handle save blueprint."""
        if not Permissions.has_permission(player, Permissions.BLUEPRINT_SAVE):
            player.send_message(Permissions.format_permission_error(Permissions.BLUEPRINT_SAVE))
            return

        clipboard_entry = self.plugin.clipboard_manager.get_latest(player.unique_id)

        if not clipboard_entry:
            player.send_message("§cClipboard is empty!§r")
            return

        success = self.plugin.blueprint_manager.save_blueprint(
            player.unique_id,
            name,
            clipboard_entry,
            description="",
            author=player.name,
            shared=False
        )

        if success:
            player.send_message(f"§aBlueprint '{name}' saved!§r")
        else:
            player.send_message(f"§cFailed to save blueprint§r")

    def handle_create_zone(self, player: "Player", name: str, radius: int, duration: float) -> None:
        """Handle create zone."""
        if not Permissions.has_permission(player, Permissions.ZONE):
            player.send_message(Permissions.format_permission_error(Permissions.ZONE))
            return

        from .selection import Position

        location = player.location
        center = Position.from_location(location)
        dimension = player.dimension.name

        zone = self.plugin.zone_manager.create_zone_at_location(
            name,
            player.name,
            center,
            dimension,
            radius,
            duration
        )

        player.send_message(f"§aCreated builder zone '{name}' (radius: {radius}, duration: {duration}h)§r")

