from typing import Optional, TYPE_CHECKING
from endstone.form import ActionForm, ModalForm, TextInput

if TYPE_CHECKING:
    from endstone import Player

class ShapeToolMenuHandler:
    def __init__(self, plugin):
        self.plugin = plugin
        # Store shape settings per player
        self.shape_settings = {}

    def show_shape_selection_menu(self, player: "Player") -> None:
        """Show shape selection menu."""
        form = ActionForm()
        form.title = "§l§6Shape Tool Configuration§r"
        form.content = "Select a shape to configure:"
        
        form.add_button("§aSphere§r")
        form.add_button("§cHollow Sphere§r")
        form.add_button("§bCylinder§r")
        form.add_button("§dHollow Cylinder§r")
        form.add_button("§eSquare§r")
        form.add_button("§6Hollow Square§r")
        form.add_button("§9Pyramid§r")
        form.add_button("§5Hollow Pyramid§r")

        def on_submit(player: "Player", data: Optional[int]):
            if data is None:
                return
            
            if data == 0:  # Sphere
                self.show_sphere_config(player, hollow=False)
            elif data == 1:  # Hollow Sphere
                self.show_sphere_config(player, hollow=True)
            elif data == 2:  # Cylinder
                self.show_cylinder_config(player, hollow=False)
            elif data == 3:  # Hollow Cylinder
                self.show_cylinder_config(player, hollow=True)
            elif data == 4:  # Square
                self.show_square_config(player, hollow=False)
            elif data == 5:  # Hollow Square
                self.show_square_config(player, hollow=True)
            elif data == 6:  # Pyramid
                self.show_pyramid_config(player, hollow=False)
            elif data == 7:  # Hollow Pyramid
                self.show_pyramid_config(player, hollow=True)

        form.on_submit = on_submit
        player.send_form(form)

    def show_sphere_config(self, player: "Player", hollow: bool) -> None:
        """Show sphere configuration form."""
        form = ModalForm()
        form.title = f"§l§{'e' if hollow else 'a'}{'Hollow ' if hollow else ''}Sphere Config§r"
        form.add_control(TextInput("Block Type:", "Example: stone, glass", "stone"))
        form.add_control(TextInput("Radius:", "Sphere radius", "5"))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                return

            import json
            values = json.loads(data)

            if not values[0] or not values[1]:
                return

            try:
                radius = int(values[1])
                self.shape_settings[player.unique_id] = {
                    "type": "hsphere" if hollow else "sphere",
                    "block": values[0].strip(),
                    "radius": radius
                }
                player.send_message(f"§aShape tool configured: {'Hollow ' if hollow else ''}Sphere ({values[0]}, radius {radius})§r")
                player.send_message("§7Right-click to spawn the shape!§r")
            except ValueError:
                player.send_message("§cInvalid radius!§r")

        form.on_submit = on_submit
        player.send_form(form)

    def show_cylinder_config(self, player: "Player", hollow: bool) -> None:
        """Show cylinder configuration form."""
        form = ModalForm()
        form.title = f"§l§{'d' if hollow else 'b'}{'Hollow ' if hollow else ''}Cylinder Config§r"
        form.add_control(TextInput("Block Type:", "Example: stone, glass", "stone"))
        form.add_control(TextInput("Radius:", "Cylinder radius", "5"))
        form.add_control(TextInput("Height:", "Cylinder height", "10"))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                return

            import json
            values = json.loads(data)

            if not values[0] or not values[1] or not values[2]:
                return

            try:
                radius = int(values[1])
                height = int(values[2])
                self.shape_settings[player.unique_id] = {
                    "type": "hcyl" if hollow else "cyl",
                    "block": values[0].strip(),
                    "radius": radius,
                    "height": height
                }
                player.send_message(f"§aShape tool configured: {'Hollow ' if hollow else ''}Cylinder ({values[0]}, radius {radius}, height {height})§r")
                player.send_message("§7Right-click to spawn the shape!§r")
            except ValueError:
                player.send_message("§cInvalid radius or height!§r")

        form.on_submit = on_submit
        player.send_form(form)

    def show_square_config(self, player: "Player", hollow: bool = False) -> None:
        """Show square configuration form."""
        form = ModalForm()
        form.title = f"§l§{'6' if hollow else 'e'}{'Hollow ' if hollow else ''}Square Configuration§r"
        form.add_control(TextInput("Block Type:", "Example: stone, glass", "stone"))
        form.add_control(TextInput("Width (X):", "Square width", "10"))
        form.add_control(TextInput("Height (Y):", "Square height", "5"))
        form.add_control(TextInput("Length (Z):", "Square length", "10"))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                return

            import json
            values = json.loads(data)

            if not values[0] or not values[1] or not values[2] or not values[3]:
                return

            block_type = values[0].strip()
            try:
                width = int(values[1])
                height = int(values[2])
                length = int(values[3])
                
                # Store configuration
                player_uuid = player.unique_id
                self.shape_settings[player_uuid] = {
                    'type': 'hsquare' if hollow else 'square',
                    'block': block_type,
                    'width': width,
                    'height': height,
                    'length': length
                }
                
                player.send_message(f"§aShape tool configured: {'Hollow ' if hollow else ''}Square ({block_type}, {width}x{height}x{length})§r")
                player.send_message("§7Right-click to spawn the shape!§r")
            except ValueError:
                player.send_message("§cInvalid dimensions! Please enter valid numbers.§r")

        form.on_submit = on_submit
        player.send_form(form)

    def show_pyramid_config(self, player: "Player", hollow: bool = False) -> None:
        """Show pyramid configuration form."""
        form = ModalForm()
        form.title = f"§l§{'5' if hollow else '9'}{'Hollow ' if hollow else ''}Pyramid Configuration§r"
        form.add_control(TextInput("Block Type:", "Example: stone, sandstone", "sandstone"))
        form.add_control(TextInput("Size:", "Base size", "10"))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                return

            import json
            values = json.loads(data)

            if not values[0] or not values[1]:
                return

            block_type = values[0].strip()
            try:
                size = int(values[1])
                
                # Store configuration
                player_uuid = player.unique_id
                self.shape_settings[player_uuid] = {
                    'type': 'hpyramid' if hollow else 'pyramid',
                    'block': block_type,
                    'size': size
                }
                
                player.send_message(f"§aShape tool configured: {'Hollow ' if hollow else ''}Pyramid ({block_type}, size {size})§r")
                player.send_message("§7Right-click to spawn the shape!§r")
            except ValueError:
                player.send_message("§cInvalid size! Please enter valid numbers.§r")

        form.on_submit = on_submit
        player.send_form(form)

    def spawn_shape_at_crosshair(self, player: "Player") -> None:
        """Spawn the configured shape at player's crosshair location."""
        player_uuid = player.unique_id
        
        if player_uuid not in self.shape_settings:
            player.send_message("§cNo shape configured! Sneak + Right-click with the shape tool to configure.§r")
            return

        settings = self.shape_settings[player_uuid]
        shape_type = settings["type"]
        
        # Get crosshair target for ALL shapes (this was the original working approach)
        target_coords = self._get_crosshair_target(player)
        if not target_coords:
            player.send_message("§cNo target block found!§r")
            return
        
        x, y, z = target_coords
        
        try:
            if shape_type in ["sphere", "hsphere"]:
                # Build sphere manually at crosshair location
                self._build_sphere(player.dimension, x, y, z, settings, shape_type == "hsphere")
            elif shape_type in ["cyl", "hcyl"]:
                # Build cylinder manually at crosshair location  
                self._build_cylinder(player.dimension, x, y, z, settings, shape_type == "hcyl")
            elif shape_type in ["pyramid", "hpyramid"]:
                # Build pyramid manually at crosshair location
                if shape_type == "hpyramid":
                    self._build_hollow_pyramid(player.dimension, x, y, z, settings)
                else:
                    self._build_pyramid(player.dimension, x, y, z, settings)
            elif shape_type in ["square", "hsquare"]:
                self._create_square_selection(player, x, y, z, settings)
                if shape_type == "hsquare":
                    player.perform_command(f"walls {settings['block']}")
                else:
                    player.perform_command(f"set {settings['block']}")
            
            player.send_message(f"§aSpawned {shape_type} at your crosshair!§r")
        except Exception as e:
            player.send_message(f"§cError spawning shape: {str(e)}§r")

    def _create_square_selection(self, player: "Player", x: int, y: int, z: int, settings: dict) -> None:
        """Create a selection for square shapes."""
        width = settings["width"]
        height = settings["height"]
        length = settings["length"]
        
        # Set selection in plugin
        player_uuid = player.unique_id
        if player_uuid not in self.plugin.selections:
            self.plugin.selections[player_uuid] = {}
        
        self.plugin.selections[player_uuid]['pos1'] = (x, y, z)
        self.plugin.selections[player_uuid]['pos2'] = (x + width - 1, y + height - 1, z + length - 1)

    def _get_crosshair_target(self, player: "Player"):
        """Get the target block coordinates the player is looking at."""
        loc = player.location
        dimension = player.dimension
        
        # Get player's eye position
        eye_x = loc.x
        eye_y = loc.y + 1.6  # Player eye height
        eye_z = loc.z
        
        # Calculate direction vector from player's rotation
        import math
        yaw = math.radians(loc.yaw)
        pitch = math.radians(loc.pitch)
        
        # Direction vector
        dx = -math.sin(yaw) * math.cos(pitch)
        dy = -math.sin(pitch)
        dz = math.cos(yaw) * math.cos(pitch)
        
        # Raycast up to 100 blocks
        max_distance = 100
        for distance in range(1, max_distance + 1):
            check_x = int(eye_x + dx * distance)
            check_y = int(eye_y + dy * distance)
            check_z = int(eye_z + dz * distance)
            
            # Check if this block is solid
            try:
                block = dimension.get_block_at(check_x, check_y, check_z)
                if block.type != "minecraft:air":
                    # Found a solid block, return the position before it
                    return (
                        int(eye_x + dx * (distance - 1)),
                        int(eye_y + dy * (distance - 1)),
                        int(eye_z + dz * (distance - 1))
                    )
            except:
                # If we can't check the block, continue
                continue
        
        # No solid block found, return position 10 blocks away
        return (
            int(eye_x + dx * 10),
            int(eye_y + dy * 10),
            int(eye_z + dz * 10)
        )

    def _build_square(self, dimension, x, y, z, settings):
        """Build a square/cube at the specified location."""
        block_type = settings["block"]
        width = settings["width"]
        height = settings["height"]
        length = settings["length"]
        
        for dx in range(width):
            for dy in range(height):
                for dz in range(length):
                    try:
                        block = dimension.get_block_at(x + dx, y + dy, z + dz)
                        block.set_type(block_type)
                    except:
                        continue

    def _build_sphere(self, dimension, center_x, center_y, center_z, settings, hollow):
        """Build a sphere at the specified location."""
        block_type = settings["block"]
        radius = settings["radius"]
        
        for x in range(center_x - radius, center_x + radius + 1):
            for y in range(center_y - radius, center_y + radius + 1):
                for z in range(center_z - radius, center_z + radius + 1):
                    distance = ((x - center_x) ** 2 + (y - center_y) ** 2 + (z - center_z) ** 2) ** 0.5
                    
                    if hollow:
                        # Hollow sphere - only place blocks on the surface
                        if abs(distance - radius) <= 0.5:
                            try:
                                block = dimension.get_block_at(x, y, z)
                                block.set_type(block_type)
                            except:
                                continue
                    else:
                        # Solid sphere
                        if distance <= radius:
                            try:
                                block = dimension.get_block_at(x, y, z)
                                block.set_type(block_type)
                            except:
                                continue

    def _build_cylinder(self, dimension, center_x, center_y, center_z, settings, hollow):
        """Build a cylinder at the specified location."""
        block_type = settings["block"]
        radius = settings["radius"]
        height = settings["height"]
        
        for x in range(center_x - radius, center_x + radius + 1):
            for y in range(center_y, center_y + height):
                for z in range(center_z - radius, center_z + radius + 1):
                    distance = ((x - center_x) ** 2 + (z - center_z) ** 2) ** 0.5
                    
                    if hollow:
                        # Hollow cylinder - only place blocks on the circumference
                        if abs(distance - radius) <= 0.5:
                            try:
                                block = dimension.get_block_at(x, y, z)
                                block.set_type(block_type)
                            except:
                                continue
                    else:
                        # Solid cylinder
                        if distance <= radius:
                            try:
                                block = dimension.get_block_at(x, y, z)
                                block.set_type(block_type)
                            except:
                                continue

    def _build_pyramid(self, dimension, base_x, base_y, base_z, settings):
        """Build a pyramid at the specified location."""
        block_type = settings["block"]
        size = settings["size"]
        
        for level in range(size):
            current_size = size - level
            y = base_y + level
            
            for x in range(base_x - current_size, base_x + current_size + 1):
                for z in range(base_z - current_size, base_z + current_size + 1):
                    try:
                        block = dimension.get_block_at(x, y, z)
                        block.set_type(block_type)
                    except:
                        continue

    def _build_hollow_pyramid(self, dimension, base_x, base_y, base_z, settings):
        """Build a hollow pyramid at the specified location."""
        block_type = settings["block"]
        size = settings["size"]
        
        for level in range(size):
            current_size = size - level
            y = base_y + level
            
            for x in range(base_x - current_size, base_x + current_size + 1):
                for z in range(base_z - current_size, base_z + current_size + 1):
                    # Only place blocks on the edges (hollow)
                    if (x == base_x - current_size or 
                        x == base_x + current_size or 
                        z == base_z - current_size or 
                        z == base_z + current_size):
                        try:
                            block = dimension.get_block_at(x, y, z)
                            block.set_type(block_type)
                        except:
                            continue


















