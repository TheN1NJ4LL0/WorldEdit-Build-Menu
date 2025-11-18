"""Menu handlers for WorldEdit Builder Menu."""

from typing import TYPE_CHECKING, Optional
from endstone.form import ActionForm, MessageForm, ModalForm, TextInput, Toggle, Dropdown

from .ui_components import UIBuilder

if TYPE_CHECKING:
    from endstone.player import Player
    from .plugin import WorldEditPlugin


class MenuHandler:
    """Handles UI menu interactions."""

    def __init__(self, plugin: "WorldEditPlugin"):
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
        form = ActionForm()
        form.title = "§l§6WorldEdit Menu§r"
        form.content = "§7Choose a category:§r"

        # Add buttons for each category
        form.add_button("§l§3Selection Tools§r\n§7Set positions & view selection§r")
        form.add_button("§l§2Clipboard§r\n§7Copy, cut, paste operations§r")
        form.add_button("§l§eEditing§r\n§7Set, replace, fill blocks§r")
        form.add_button("§l§dShapes§r\n§7Create spheres, cylinders§r")
        form.add_button("§l§9Schematics§r\n§7Save & load builds§r")
        form.add_button("§l§5Build Areas§r\n§7Manage your build areas§r")
        form.add_button("§l§6Undo/Redo§r\n§7Undo or redo changes§r")
        form.add_button("§l§cClose§r")

        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return

            if data == 0:  # Selection
                self.show_selection_menu(player)
            elif data == 1:  # Clipboard
                self.show_clipboard_menu(player)
            elif data == 2:  # Editing
                self.show_editing_menu(player)
            elif data == 3:  # Shapes
                self.show_shapes_menu(player)
            elif data == 4:  # Schematics
                self.show_schematic_menu(player)
            elif data == 5:  # Build Areas
                self.show_build_areas_menu(player)
            elif data == 6:  # Undo/Redo
                self.show_undo_menu(player)
            # data == 7 is Close, do nothing

        form.on_submit = on_submit
        player.send_form(form)
    
    def show_selection_menu(self, player: "Player") -> None:
        """Show selection menu.

        Args:
            player: Player to show menu to
        """
        uuid = str(player.unique_id)
        has_pos1 = uuid in self.plugin.selections and "pos1" in self.plugin.selections[uuid]
        has_pos2 = uuid in self.plugin.selections and "pos2" in self.plugin.selections[uuid]

        content = "§7Current Selection:§r\n"
        if has_pos1:
            pos1 = self.plugin.selections[uuid]["pos1"]
            content += f"§aPos1: §f{pos1[0]}, {pos1[1]}, {pos1[2]}§r\n"
        else:
            content += "§7Pos1: Not set§r\n"

        if has_pos2:
            pos2 = self.plugin.selections[uuid]["pos2"]
            content += f"§aPos2: §f{pos2[0]}, {pos2[1]}, {pos2[2]}§r\n"
        else:
            content += "§7Pos2: Not set§r\n"

        if has_pos1 and has_pos2:
            # Calculate volume
            pos1 = self.plugin.selections[uuid]["pos1"]
            pos2 = self.plugin.selections[uuid]["pos2"]
            dx = abs(pos2[0] - pos1[0]) + 1
            dy = abs(pos2[1] - pos1[1]) + 1
            dz = abs(pos2[2] - pos1[2]) + 1
            volume = dx * dy * dz
            content += f"§eVolume: §f{volume} blocks§r"

        form = ActionForm()
        form.title = "§l§3Selection Tools§r"
        form.content = content

        form.add_button("§aSet Position 1§r\n§7At your location§r")
        form.add_button("§aSet Position 2§r\n§7At your location§r")
        form.add_button("§eGet Selection Wand§r\n§7Left/Right click blocks§r")
        if has_pos1 and has_pos2:
            form.add_button("§cClear Selection§r")
        form.add_button("§7« Back to Main Menu§r")

        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return

            if data == 0:  # Set pos1
                loc = player.location
                pos = (int(loc.x), int(loc.y), int(loc.z))
                if uuid not in self.plugin.selections:
                    self.plugin.selections[uuid] = {}
                self.plugin.selections[uuid]["pos1"] = pos
                player.send_message(f"§aPosition 1 set to {pos[0]}, {pos[1]}, {pos[2]}§r")
                self.show_selection_menu(player)
            elif data == 1:  # Set pos2
                loc = player.location
                pos = (int(loc.x), int(loc.y), int(loc.z))
                if uuid not in self.plugin.selections:
                    self.plugin.selections[uuid] = {}
                self.plugin.selections[uuid]["pos2"] = pos
                player.send_message(f"§aPosition 2 set to {pos[0]}, {pos[1]}, {pos[2]}§r")
                self.show_selection_menu(player)
            elif data == 2:  # Get wand
                player.perform_command("wand")
                self.show_selection_menu(player)
            elif data == 3:  # Clear or Back
                if has_pos1 and has_pos2:
                    if uuid in self.plugin.selections:
                        self.plugin.selections[uuid].clear()
                    player.send_message("§aSelection cleared§r")
                    self.show_selection_menu(player)
                else:
                    self.show_main_menu(player)
            elif data == 4:  # Back
                self.show_main_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_clipboard_menu(self, player: "Player") -> None:
        """Show clipboard menu.

        Args:
            player: Player to show menu to
        """
        uuid = str(player.unique_id)
        has_clipboard = uuid in self.plugin.clipboard
        has_selection = uuid in self.plugin.selections and "pos1" in self.plugin.selections[uuid] and "pos2" in self.plugin.selections[uuid]

        content = "§7Clipboard Operations§r\n"
        if has_clipboard:
            content += "§aClipboard: §fHas data§r\n"
        else:
            content += "§7Clipboard: Empty§r\n"

        if not has_selection:
            content += "§c⚠ No selection made§r"

        form = ActionForm()
        form.title = "§l§2Clipboard§r"
        form.content = content

        form.add_button("§aCopy§r\n§7Copy selection (no air)§r")
        form.add_button("§eCut§r\n§7Cut selection to clipboard§r")
        form.add_button("§bPaste§r\n§7Paste clipboard (no air)§r")
        form.add_button("§dCopy Options§r\n§7Copy with air/entities§r")
        form.add_button("§5Paste Options§r\n§7Paste with air blocks§r")
        form.add_button("§7« Back to Main Menu§r")

        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return

            if data == 0:  # Copy
                if not has_selection:
                    player.send_message("§cYou need to make a selection first!§r")
                    self.show_clipboard_menu(player)
                    return
                player.perform_command("copy")
                self.show_clipboard_menu(player)
            elif data == 1:  # Cut
                if not has_selection:
                    player.send_message("§cYou need to make a selection first!§r")
                    self.show_clipboard_menu(player)
                    return
                player.perform_command("cut")
                self.show_clipboard_menu(player)
            elif data == 2:  # Paste
                if not has_clipboard:
                    player.send_message("§cYour clipboard is empty!§r")
                    self.show_clipboard_menu(player)
                    return
                player.perform_command("paste")
                self.show_clipboard_menu(player)
            elif data == 3:  # Copy Options
                if not has_selection:
                    player.send_message("§cYou need to make a selection first!§r")
                    self.show_clipboard_menu(player)
                    return
                self.show_copy_options_form(player)
            elif data == 4:  # Paste Options
                if not has_clipboard:
                    player.send_message("§cYour clipboard is empty!§r")
                    self.show_clipboard_menu(player)
                    return
                self.show_paste_options_form(player)
            else:  # Back
                self.show_main_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_copy_options_form(self, player: "Player") -> None:
        """Show copy options form.

        Args:
            player: Player to show menu to
        """
        form = ModalForm()
        form.title = "§l§dCopy Options§r"
        form.add_control(Toggle("Include Air Blocks", False))
        form.add_control(Toggle("Copy Entities", False))
        form.add_control(Toggle("Copy Biomes", False))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                self.show_clipboard_menu(player)
                return

            import json
            values = json.loads(data)
            include_air = values[0] if len(values) > 0 else False
            copy_entities = values[1] if len(values) > 1 else False
            copy_biomes = values[2] if len(values) > 2 else False

            # Build command with flags
            cmd = "copy"
            if include_air:
                cmd += " -a"
            if copy_entities:
                cmd += " -e"
            if copy_biomes:
                cmd += " -b"

            player.perform_command(cmd)
            player.send_message("§aCopied with options!§r")
            self.show_clipboard_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_editing_menu(self, player: "Player") -> None:
        """Show editing menu.

        Args:
            player: Player to show menu to
        """
        uuid = str(player.unique_id)
        has_selection = uuid in self.plugin.selections and "pos1" in self.plugin.selections[uuid] and "pos2" in self.plugin.selections[uuid]

        content = "§7Block Editing Operations§r\n"
        if not has_selection:
            content += "§c⚠ No selection made§r"

        form = ActionForm()
        form.title = "§l§eEditing§r"
        form.content = content

        form.add_button("§aSet Blocks§r\n§7Fill selection with block§r")
        form.add_button("§eReplace Blocks§r\n§7Replace blocks in selection§r")
        form.add_button("§bWalls§r\n§7Create walls around selection§r")
        form.add_button("§dOverlay§r\n§7Place blocks on top§r")
        form.add_button("§7« Back to Main Menu§r")

        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return

            if data == 0:  # Set
                if not has_selection:
                    player.send_message("§cYou need to make a selection first!§r")
                    self.show_editing_menu(player)
                    return
                self.show_set_blocks_form(player)
            elif data == 1:  # Replace
                if not has_selection:
                    player.send_message("§cYou need to make a selection first!§r")
                    self.show_editing_menu(player)
                    return
                self.show_replace_blocks_form(player)
            elif data == 2:  # Walls
                if not has_selection:
                    player.send_message("§cYou need to make a selection first!§r")
                    self.show_editing_menu(player)
                    return
                self.show_walls_form(player)
            elif data == 3:  # Overlay
                if not has_selection:
                    player.send_message("§cYou need to make a selection first!§r")
                    self.show_editing_menu(player)
                    return
                self.show_overlay_form(player)
            else:  # Back
                self.show_main_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_set_blocks_form(self, player: "Player") -> None:
        """Show set blocks form.

        Args:
            player: Player to show menu to
        """
        form = ModalForm()
        form.title = "§l§aSet Blocks§r"
        form.add_control(TextInput("Block Type:", "Example: stone, grass, diamond_block", "stone"))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                self.show_editing_menu(player)
                return

            import json
            values = json.loads(data)

            if not values[0]:
                self.show_editing_menu(player)
                return

            block_type = values[0].strip()
            player.perform_command(f"set {block_type}")
            self.show_editing_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_replace_blocks_form(self, player: "Player") -> None:
        """Show replace blocks form.

        Args:
            player: Player to show menu to
        """
        form = ModalForm()
        form.title = "§l§eReplace Blocks§r"
        form.add_control(TextInput("From Block:", "Block to replace", "stone"))
        form.add_control(TextInput("To Block:", "New block type", "grass"))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                self.show_editing_menu(player)
                return

            import json
            values = json.loads(data)

            if not values[0] or not values[1]:
                self.show_editing_menu(player)
                return

            from_block = values[0].strip()
            to_block = values[1].strip()
            player.perform_command(f"replace {from_block} {to_block}")
            self.show_editing_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_walls_form(self, player: "Player") -> None:
        """Show walls form.

        Args:
            player: Player to show menu to
        """
        form = ModalForm()
        form.title = "§l§bWalls§r"
        form.add_control(TextInput("Block Type:", "Example: stone, brick", "stone"))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                self.show_editing_menu(player)
                return

            import json
            values = json.loads(data)

            if not values[0]:
                self.show_editing_menu(player)
                return

            block_type = values[0].strip()
            player.perform_command(f"walls {block_type}")
            self.show_editing_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_overlay_form(self, player: "Player") -> None:
        """Show overlay form.

        Args:
            player: Player to show menu to
        """
        form = ModalForm()
        form.title = "§l§dOverlay§r"
        form.add_control(TextInput("Block Type:", "Example: grass, snow", "grass"))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                self.show_editing_menu(player)
                return

            import json
            values = json.loads(data)

            if not values[0]:
                self.show_editing_menu(player)
                return

            block_type = values[0].strip()
            player.perform_command(f"overlay {block_type}")
            self.show_editing_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_shapes_menu(self, player: "Player") -> None:
        """Show shapes menu.

        Args:
            player: Player to show menu to
        """
        form = ActionForm()
        form.title = "§l§dShapes§r"
        form.content = "§7Create geometric shapes§r"

        form.add_button("§aSphere§r\n§7Create a filled sphere§r")
        form.add_button("§eHollow Sphere§r\n§7Create a hollow sphere§r")
        form.add_button("§bCylinder§r\n§7Create a filled cylinder§r")
        form.add_button("§dHollow Cylinder§r\n§7Create a hollow cylinder§r")
        form.add_button("§7« Back to Main Menu§r")

        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return

            if data == 0:  # Sphere
                self.show_sphere_form(player, False)
            elif data == 1:  # Hollow Sphere
                self.show_sphere_form(player, True)
            elif data == 2:  # Cylinder
                self.show_cylinder_form(player, False)
            elif data == 3:  # Hollow Cylinder
                self.show_cylinder_form(player, True)
            else:  # Back
                self.show_main_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_sphere_form(self, player: "Player", hollow: bool) -> None:
        """Show sphere creation form.

        Args:
            player: Player to show menu to
            hollow: Whether to create hollow sphere
        """
        form = ModalForm()
        form.title = f"§l§{'e' if hollow else 'a'}{'Hollow ' if hollow else ''}Sphere§r"
        form.add_control(TextInput("Block Type:", "Example: stone, glass", "stone"))
        form.add_control(TextInput("Radius:", "Sphere radius", "5"))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                self.show_shapes_menu(player)
                return

            import json
            values = json.loads(data)

            if not values[0] or not values[1]:
                self.show_shapes_menu(player)
                return

            block_type = values[0].strip()
            try:
                radius = int(values[1])
                cmd = f"hsphere {block_type} {radius}" if hollow else f"sphere {block_type} {radius}"
                player.perform_command(cmd)
            except ValueError:
                player.send_message("§cInvalid radius!§r")
            self.show_shapes_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_cylinder_form(self, player: "Player", hollow: bool) -> None:
        """Show cylinder creation form.

        Args:
            player: Player to show menu to
            hollow: Whether to create hollow cylinder
        """
        form = ModalForm()
        form.title = f"§l§{'d' if hollow else 'b'}{'Hollow ' if hollow else ''}Cylinder§r"
        form.add_control(TextInput("Block Type:", "Example: stone, glass", "stone"))
        form.add_control(TextInput("Radius:", "Cylinder radius", "5"))
        form.add_control(TextInput("Height:", "Cylinder height", "10"))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                self.show_shapes_menu(player)
                return

            import json
            values = json.loads(data)

            if not values[0] or not values[1] or not values[2]:
                self.show_shapes_menu(player)
                return

            block_type = values[0].strip()
            try:
                radius = int(values[1])
                height = int(values[2])
                cmd = f"hcyl {block_type} {radius} {height}" if hollow else f"cyl {block_type} {radius} {height}"
                player.perform_command(cmd)
            except ValueError:
                player.send_message("§cInvalid radius or height!§r")
            self.show_shapes_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_schematic_menu(self, player: "Player") -> None:
        """Show schematic menu.

        Args:
            player: Player to show menu to
        """
        uuid = str(player.unique_id)
        has_selection = uuid in self.plugin.selections and "pos1" in self.plugin.selections[uuid] and "pos2" in self.plugin.selections[uuid]

        content = "§7Save and load schematics§r\n"
        if not has_selection:
            content += "§c⚠ No selection (needed for save)§r"

        form = ActionForm()
        form.title = "§l§9Schematics§r"
        form.content = content

        form.add_button("§aSave Schematic§r\n§7Save selection as .schem§r")
        form.add_button("§bLoad Schematic§r\n§7Load .schem file§r")
        form.add_button("§7« Back to Main Menu§r")

        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return

            if data == 0:  # Save
                if not has_selection:
                    player.send_message("§cYou need to make a selection first!§r")
                    self.show_schematic_menu(player)
                    return
                self.show_save_schematic_form(player)
            elif data == 1:  # Load
                self.show_load_schematic_form(player)
            else:  # Back
                self.show_main_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_save_schematic_form(self, player: "Player") -> None:
        """Show save schematic form.

        Args:
            player: Player to show menu to
        """
        form = ModalForm()
        form.title = "§l§aSave Schematic§r"
        form.add_control(TextInput("Filename:", "Without .schem extension", "my_build"))
        form.add_control(Toggle("Include Air Blocks", False))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                self.show_schematic_menu(player)
                return

            import json
            values = json.loads(data)

            if not values[0]:
                self.show_schematic_menu(player)
                return

            filename = values[0].strip()
            include_air = values[1] if len(values) > 1 else False

            # Build command with air flag if needed
            cmd = f"schem save {filename}"
            if include_air:
                cmd += " -a"  # Add air flag

            player.perform_command(cmd)
            self.show_schematic_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_load_schematic_form(self, player: "Player") -> None:
        """Show load schematic form.

        Args:
            player: Player to show menu to
        """
        form = ActionForm()
        form.title = "§l§bLoad Schematic§r"
        form.content = "§7Choose how to load the schematic:§r"

        form.add_button("§aQuick Load§r\n§7Load to clipboard only§r")
        form.add_button("§bLoad & Place§r\n§7Load and place with options§r")
        form.add_button("§7« Back§r")

        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                self.show_schematic_menu(player)
                return

            if data == 0:  # Quick load
                self.show_quick_load_form(player)
            elif data == 1:  # Load & Place
                self.show_load_and_place_form(player)
            else:  # Back
                self.show_schematic_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_quick_load_form(self, player: "Player") -> None:
        """Show quick load form (load to clipboard only).

        Args:
            player: Player to show menu to
        """
        form = ModalForm()
        form.title = "§l§aQuick Load§r"
        form.add_control(TextInput("Filename:", "Without .schem extension", "my_build"))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                self.show_schematic_menu(player)
                return

            import json
            values = json.loads(data)

            if not values[0]:
                self.show_schematic_menu(player)
                return

            filename = values[0].strip()
            player.perform_command(f"schem load {filename}")
            player.send_message("§aSchematic loaded to clipboard! Use Paste Options to place it.§r")
            self.show_schematic_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_load_and_place_form(self, player: "Player") -> None:
        """Show load and place form with full control.

        Args:
            player: Player to show menu to
        """
        form = ModalForm()
        form.title = "§l§bLoad & Place Schematic§r"

        # Filename
        form.add_control(TextInput("Filename:", "Without .schem extension", "my_build"))

        # Rotation
        form.add_control(Dropdown("Rotation:", ["0° (No rotation)", "90° (Clockwise)", "180°", "270° (Counter-clockwise)"], 0))

        # Flip options
        form.add_control(Toggle("Flip X (East/West)", False))
        form.add_control(Toggle("Flip Y (Up/Down)", False))
        form.add_control(Toggle("Flip Z (North/South)", False))

        # Placement position
        form.add_control(Dropdown("Place At:", ["Current Position", "In Front (3 blocks)", "In Front (5 blocks)", "In Front (10 blocks)", "Custom Offset"], 0))

        # Custom offset (only used if "Custom Offset" selected)
        form.add_control(TextInput("Custom Offset X:", "East(+) / West(-)", "0"))
        form.add_control(TextInput("Custom Offset Y:", "Up(+) / Down(-)", "0"))
        form.add_control(TextInput("Custom Offset Z:", "South(+) / North(-)", "0"))

        # Additional options
        form.add_control(Toggle("Include Air Blocks", True))
        form.add_control(Toggle("Paste Entities", True))
        form.add_control(Toggle("Paste Biomes", False))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                self.show_schematic_menu(player)
                return

            import json
            values = json.loads(data)

            if not values[0]:
                self.show_schematic_menu(player)
                return

            try:
                # Parse filename
                filename = values[0].strip()

                # Parse rotation
                rotation = values[1] if len(values) > 1 else 0
                rotation_degrees = [0, 90, 180, 270][rotation]

                # Parse flips
                flip_x = values[2] if len(values) > 2 else False
                flip_y = values[3] if len(values) > 3 else False
                flip_z = values[4] if len(values) > 4 else False

                # Parse placement position
                placement = values[5] if len(values) > 5 else 0

                # Parse custom offsets
                custom_x = int(values[6]) if len(values) > 6 and values[6] else 0
                custom_y = int(values[7]) if len(values) > 7 and values[7] else 0
                custom_z = int(values[8]) if len(values) > 8 and values[8] else 0

                # Calculate offset based on placement choice
                offset_x, offset_y, offset_z = 0, 0, 0

                if placement == 1:  # In front 3 blocks
                    # Get player's facing direction and place in front
                    offset_z = 3  # Simplified - in real implementation, use player.location.yaw
                elif placement == 2:  # In front 5 blocks
                    offset_z = 5
                elif placement == 3:  # In front 10 blocks
                    offset_z = 10
                elif placement == 4:  # Custom offset
                    offset_x = custom_x
                    offset_y = custom_y
                    offset_z = custom_z

                # Parse additional options
                include_air = values[9] if len(values) > 9 else True
                paste_entities = values[10] if len(values) > 10 else True
                paste_biomes = values[11] if len(values) > 11 else False

                # First, load the schematic
                player.perform_command(f"schem load {filename}")

                # Wait a moment, then paste with options
                # Build paste command
                cmd = "paste"

                # Add rotation
                if rotation_degrees > 0:
                    cmd += f" -r {rotation_degrees}"

                # Add flips
                if flip_x:
                    cmd += " -fx"
                if flip_y:
                    cmd += " -fy"
                if flip_z:
                    cmd += " -fz"

                # Add offset
                if offset_x != 0 or offset_y != 0 or offset_z != 0:
                    cmd += f" -o {offset_x},{offset_y},{offset_z}"

                # Add other options
                if include_air:
                    cmd += " -a"
                if paste_entities:
                    cmd += " -e"
                if paste_biomes:
                    cmd += " -b"

                # Execute paste command
                player.perform_command(cmd)

                placement_text = ["at your position", "3 blocks in front", "5 blocks in front", "10 blocks in front", f"at offset ({offset_x}, {offset_y}, {offset_z})"][placement]
                player.send_message(f"§aSchematic '{filename}' placed {placement_text} with {rotation_degrees}° rotation!§r")
                self.show_schematic_menu(player)

            except (ValueError, IndexError) as e:
                player.send_message(f"§cInvalid input! Please check your values.§r")
                self.show_schematic_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_build_areas_menu(self, player: "Player") -> None:
        """Show build areas menu.

        Args:
            player: Player to show menu to
        """
        form = ActionForm()
        form.title = "§l§5Build Areas§r"
        form.content = "§7Manage your build areas§r"

        form.add_button("§aMy Build Areas§r\n§7List your areas§r")
        form.add_button("§bCurrent Area Info§r\n§7Info about current area§r")
        form.add_button("§7« Back to Main Menu§r")

        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return

            if data == 0:  # My areas
                player.perform_command("myareas")
                self.show_build_areas_menu(player)
            elif data == 1:  # Area info
                player.perform_command("areainfo")
                self.show_build_areas_menu(player)
            else:  # Back
                self.show_main_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_undo_menu(self, player: "Player") -> None:
        """Show undo/redo menu.

        Args:
            player: Player to show menu to
        """
        uuid = str(player.unique_id)
        has_undo = uuid in self.plugin.undo_history and len(self.plugin.undo_history[uuid]) > 0
        has_redo = uuid in self.plugin.redo_history and len(self.plugin.redo_history[uuid]) > 0

        content = "§7Undo or redo your changes§r\n"
        if has_undo:
            undo_count = len(self.plugin.undo_history[uuid])
            content += f"§aUndo available: §f{undo_count} action(s)§r\n"
        else:
            content += "§7No undo history§r\n"

        if has_redo:
            redo_count = len(self.plugin.redo_history[uuid])
            content += f"§bRedo available: §f{redo_count} action(s)§r"
        else:
            content += "§7No redo history§r"

        form = ActionForm()
        form.title = "§l§6Undo/Redo§r"
        form.content = content

        form.add_button("§aUndo§r\n§7Undo last action§r")
        form.add_button("§bRedo§r\n§7Redo last undone action§r")
        form.add_button("§7« Back to Main Menu§r")

        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return

            if data == 0:  # Undo
                if not has_undo:
                    player.send_message("§cNothing to undo!§r")
                    self.show_undo_menu(player)
                    return
                player.perform_command("undo")
                self.show_undo_menu(player)
            elif data == 1:  # Redo
                if not has_redo:
                    player.send_message("§cNothing to redo!§r")
                    self.show_undo_menu(player)
                    return
                player.perform_command("redo")
                self.show_undo_menu(player)
            else:  # Back
                self.show_main_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

    def show_paste_options_form(self, player: "Player") -> None:
        """Show paste options form.

        Args:
            player: Player to show menu to
        """
        form = ModalForm()
        form.title = "§l§5Advanced Paste Options§r"

        # Rotation
        form.add_control(Dropdown("Rotation:", ["0° (No rotation)", "90° (Clockwise)", "180°", "270° (Counter-clockwise)"], 0))

        # Flip options
        form.add_control(Toggle("Flip X (East/West)", False))
        form.add_control(Toggle("Flip Y (Up/Down)", False))
        form.add_control(Toggle("Flip Z (North/South)", False))

        # Offset from player position
        form.add_control(TextInput("Offset X (blocks):", "East(+) / West(-)", "0"))
        form.add_control(TextInput("Offset Y (blocks):", "Up(+) / Down(-)", "0"))
        form.add_control(TextInput("Offset Z (blocks):", "South(+) / North(-)", "0"))

        # Additional options
        form.add_control(Toggle("Include Air Blocks", False))
        form.add_control(Toggle("Paste Entities", False))
        form.add_control(Toggle("Paste Biomes", False))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                self.show_clipboard_menu(player)
                return

            try:
                # Parse rotation


                import json

                values = json.loads(data)

                rotation = values[0] if len(data) > 0 else 0
                rotation_degrees = [0, 90, 180, 270][rotation]

                # Parse flips
                flip_x = values[1] if len(data) > 1 else False
                flip_y = values[2] if len(data) > 2 else False
                flip_z = values[3] if len(data) > 3 else False

                # Parse offsets
                offset_x = int(values[4]) if len(data) > 4 and values[4] else 0
                offset_y = int(values[5]) if len(data) > 5 and values[5] else 0
                offset_z = int(values[6]) if len(data) > 6 and values[6] else 0

                # Parse additional options
                include_air = values[7] if len(data) > 7 else False
                paste_entities = values[8] if len(data) > 8 else False
                paste_biomes = values[9] if len(data) > 9 else False

                # Build command
                cmd = "paste"

                # Add rotation
                if rotation_degrees > 0:
                    cmd += f" -r {rotation_degrees}"

                # Add flips
                if flip_x:
                    cmd += " -fx"
                if flip_y:
                    cmd += " -fy"
                if flip_z:
                    cmd += " -fz"

                # Add offset
                if offset_x != 0 or offset_y != 0 or offset_z != 0:
                    cmd += f" -o {offset_x},{offset_y},{offset_z}"

                # Add other options
                if include_air:
                    cmd += " -a"
                if paste_entities:
                    cmd += " -e"
                if paste_biomes:
                    cmd += " -b"

                player.perform_command(cmd)
                player.send_message(f"§aPasted with rotation: {rotation_degrees}°, offset: ({offset_x}, {offset_y}, {offset_z})§r")
                self.show_clipboard_menu(player)

            except (ValueError, IndexError) as e:
                player.send_message(f"§cInvalid input! Please check your values.§r")
                self.show_clipboard_menu(player)

        form.on_submit = on_submit
        player.send_form(form)

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

        form.on_submit = on_submit
        player.send_form(form)

    def show_save_blueprint_form(self, player: "Player") -> None:
        """Show save blueprint form.
        
        Args:
            player: Player to show menu to
        """
        form = UIBuilder.create_input_form("§l§2Save Blueprint§r", "Blueprint Name:", "my_build")
        
        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                return

            import json
            values = json.loads(data)

            if not values[0]:
                return

            name = values[0].strip()
            self.handle_save_blueprint(player, name)

        form.on_submit = on_submit
        player.send_form(form)

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

        form.on_submit = on_submit
        player.send_form(form)

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
        
        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                return

            import json
            values = json.loads(data)

            if not values[0]:
                return

            name = values[0].strip()
            radius = int(values[1])
            duration = float(values[2])

            self.handle_create_zone(player, name, radius, duration)

        form.on_submit = on_submit
        player.send_form(form)

    # Handler methods
    def handle_set_pos1(self, player: "Player") -> None:
        """Handle set position 1."""
        location = player.location
        pos = (int(location.x), int(location.y), int(location.z))
        dimension = player.dimension.name

        if player.unique_id not in self.plugin.selections:
            self.plugin.selections[player.unique_id] = {}

        self.plugin.selections[player.unique_id]['pos1'] = pos
        self.plugin.selections[player.unique_id]['dimension'] = dimension

        player.send_message(f"§aPosition 1 set to ({pos[0]}, {pos[1]}, {pos[2]})§r")

        if 'pos2' in self.plugin.selections[player.unique_id]:
            pos2 = self.plugin.selections[player.unique_id]['pos2']
            volume = abs((pos2[0] - pos[0] + 1) * (pos2[1] - pos[1] + 1) * (pos2[2] - pos[2] + 1))
            player.send_message(f"§7Selection: {volume} blocks§r")

    def handle_set_pos2(self, player: "Player") -> None:
        """Handle set position 2."""
        location = player.location
        pos = (int(location.x), int(location.y), int(location.z))
        dimension = player.dimension.name

        if player.unique_id not in self.plugin.selections:
            self.plugin.selections[player.unique_id] = {}

        self.plugin.selections[player.unique_id]['pos2'] = pos
        self.plugin.selections[player.unique_id]['dimension'] = dimension

        player.send_message(f"§aPosition 2 set to ({pos[0]}, {pos[1]}, {pos[2]})§r")

        if 'pos1' in self.plugin.selections[player.unique_id]:
            pos1 = self.plugin.selections[player.unique_id]['pos1']
            volume = abs((pos[0] - pos1[0] + 1) * (pos[1] - pos1[1] + 1) * (pos[2] - pos1[2] + 1))
            player.send_message(f"§7Selection: {volume} blocks§r")

    def handle_copy(self, player: "Player") -> None:
        """Handle copy operation."""
        player_uuid = player.unique_id

        if player_uuid not in self.plugin.selections:
            player.send_message("§cNo selection! Use /builder pos1 and /builder pos2§r")
            return

        selection = self.plugin.selections[player_uuid]
        if 'pos1' not in selection or 'pos2' not in selection:
            player.send_message("§cNo selection! Use /builder pos1 and /builder pos2§r")
            return

        pos1 = selection['pos1']
        pos2 = selection['pos2']
        dimension = player.dimension

        # Calculate bounds
        min_x, max_x = min(pos1[0], pos2[0]), max(pos1[0], pos2[0])
        min_y, max_y = min(pos1[1], pos2[1]), max(pos1[1], pos2[1])
        min_z, max_z = min(pos1[2], pos2[2]), max(pos1[2], pos2[2])

        # Copy blocks
        blocks = []
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                for x in range(min_x, max_x + 1):
                    block = dimension.get_block_at(x, y, z)
                    blocks.append({
                        'type': block.type,
                        'data': block.data if hasattr(block, 'data') else 0
                    })

        # Store in clipboard
        self.plugin.clipboard[player_uuid] = {
            'blocks': blocks,
            'dimensions': (max_x - min_x + 1, max_y - min_y + 1, max_z - min_z + 1),
            'origin': pos1
        }

        player.send_message(f"§aCopied {len(blocks)} blocks to clipboard§r")

    def handle_cut(self, player: "Player") -> None:
        """Handle cut operation."""
        # First copy
        self.handle_copy(player)

        player_uuid = player.unique_id
        if player_uuid not in self.plugin.selections:
            return

        selection = self.plugin.selections[player_uuid]
        if 'pos1' not in selection or 'pos2' not in selection:
            return

        pos1 = selection['pos1']
        pos2 = selection['pos2']
        dimension = player.dimension

        # Calculate bounds
        min_x, max_x = min(pos1[0], pos2[0]), max(pos1[0], pos2[0])
        min_y, max_y = min(pos1[1], pos2[1]), max(pos1[1], pos2[1])
        min_z, max_z = min(pos1[2], pos2[2]), max(pos1[2], pos2[2])

        # Replace with air
        count = 0
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                for x in range(min_x, max_x + 1):
                    block = dimension.get_block_at(x, y, z)
                    block.set_type("minecraft:air")
                    count += 1

        player.send_message(f"§aCut {count} blocks§r")

    def handle_paste(self, player: "Player", options=None) -> None:
        """Handle paste operation."""
        player_uuid = player.unique_id

        if player_uuid not in self.plugin.clipboard:
            player.send_message("§cClipboard is empty!§r")
            return

        clipboard = self.plugin.clipboard[player_uuid]
        blocks = clipboard['blocks']
        dimensions = clipboard['dimensions']

        # Get target position
        location = player.location
        target_x, target_y, target_z = int(location.x), int(location.y), int(location.z)
        dimension = player.dimension

        player.send_message("§7Pasting...§r")

        # Paste blocks
        width, height, length = dimensions
        idx = 0
        placed = 0

        for y in range(height):
            for z in range(length):
                for x in range(width):
                    if idx < len(blocks):
                        block_data = blocks[idx]
                        world_x = target_x + x
                        world_y = target_y + y
                        world_z = target_z + z

                        try:
                            block = dimension.get_block_at(world_x, world_y, world_z)
                            block.set_type(block_data['type'])
                            if 'data' in block_data and hasattr(block, 'set_data'):
                                block.set_data(block_data['data'])
                            placed += 1
                        except Exception as e:
                            pass  # Skip blocks that can't be placed

                        idx += 1

        player.send_message(f"§aPasted {placed} blocks§r")

    def handle_undo(self, player: "Player") -> None:
        """Handle undo operation."""
        player_uuid = player.unique_id

        if player_uuid not in self.plugin.undo_history or not self.plugin.undo_history[player_uuid]:
            player.send_message("§cNothing to undo§r")
            return

        # Use WorldEdit's existing undo system
        undo_data = self.plugin.undo_history[player_uuid].pop()
        dimension = player.dimension

        # Restore blocks
        count = 0
        for block_info in undo_data:
            try:
                x, y, z = block_info['pos']
                block = dimension.get_block_at(x, y, z)
                block.set_type(block_info['type'])
                if 'data' in block_info and hasattr(block, 'set_data'):
                    block.set_data(block_info['data'])
                count += 1
            except:
                pass

        player.send_message(f"§aUndone {count} blocks§r")

    def handle_save_blueprint(self, player: "Player", name: str) -> None:
        """Handle save blueprint."""
        player_uuid = player.unique_id

        if player_uuid not in self.plugin.clipboard:
            player.send_message("§cClipboard is empty!§r")
            return

        clipboard = self.plugin.clipboard[player_uuid]

        # Save blueprint using blueprint manager
        try:
            import json
            import os

            blueprint_dir = f"plugins/WorldEdit/blueprints/{player_uuid}"
            os.makedirs(blueprint_dir, exist_ok=True)

            blueprint_path = os.path.join(blueprint_dir, f"{name}.json")

            with open(blueprint_path, 'w') as f:
                json.dump(clipboard, f, indent=2)

            player.send_message(f"§aBlueprint '{name}' saved!§r")
        except Exception as e:
            player.send_message(f"§cFailed to save blueprint: {e}§r")

    def handle_create_zone(self, player: "Player", name: str, radius: int, duration: float) -> None:
        """Handle create zone."""
        if not player.is_op:
            player.send_message("§cOnly operators can create zones!§r")
            return

        location = player.location
        center_x, center_y, center_z = int(location.x), int(location.y), int(location.z)
        dimension = player.dimension.name

        # Create zone using build area manager
        min_x, min_y, min_z = center_x - radius, center_y - radius, center_z - radius
        max_x, max_y, max_z = center_x + radius, center_y + radius, center_z + radius

        self.plugin.build_area_manager.create_area(
            name,
            dimension,
            min_x, min_y, min_z,
            max_x, max_y, max_z,
            [player.name]
        )

        player.send_message(f"§aCreated builder zone '{name}' (radius: {radius})§r")

