from typing import Optional, TYPE_CHECKING
from endstone.form import ModalForm, TextInput, Dropdown, Toggle

if TYPE_CHECKING:
    from endstone import Player

class SmoothToolMenuHandler:
    def __init__(self, plugin):
        self.plugin = plugin
        # Store smooth settings per player
        self.smooth_settings = {}

    def show_smooth_config_menu(self, player: "Player") -> None:
        """Show smooth tool configuration menu."""
        # Get current settings if they exist
        uuid = player.unique_id
        current_settings = self.smooth_settings.get(uuid, {})
        current_radius = str(current_settings.get('radius', 5))
        current_iterations_index = {1: 0, 2: 1, 3: 2, 5: 3, 7: 4, 10: 5}.get(current_settings.get('iterations', 3), 2)
        current_use_selection = current_settings.get('use_selection', False)

        form = ModalForm()
        form.title = "§l§6Smooth Tool Configuration§r"

        # Configuration options
        form.add_control(TextInput("Radius:", "Area radius to smooth (1-20)", current_radius))
        form.add_control(Dropdown("Aggressiveness:", [
            "Gentle (1 iteration)",
            "Light (2 iterations)",
            "Medium (3 iterations)",
            "Strong (5 iterations)",
            "Very Strong (7 iterations)",
            "Extreme (10 iterations)"
        ], current_iterations_index))
        form.add_control(Toggle("Use Current Selection", current_use_selection))

        def on_submit(player: "Player", data: Optional[str]):
            if data is None:
                return

            import json
            values = json.loads(data)

            if not values[0]:
                return

            try:
                radius = int(values[0])
                if radius < 1 or radius > 20:
                    player.send_message("§cRadius must be between 1 and 20!§r")
                    return

                # Map dropdown to iterations
                aggressiveness_map = [1, 2, 3, 5, 7, 10]
                aggressiveness_index = values[1] if len(values) > 1 else 2
                iterations = aggressiveness_map[aggressiveness_index]

                use_selection = values[2] if len(values) > 2 else False

                # Save settings
                uuid = player.unique_id
                self.smooth_settings[uuid] = {
                    'radius': radius,
                    'iterations': iterations,
                    'use_selection': use_selection
                }

                # Show confirmation
                mode_text = "current selection" if use_selection else f"{radius} block radius"
                aggressiveness_names = ["Gentle", "Light", "Medium", "Strong", "Very Strong", "Extreme"]
                aggressiveness_text = aggressiveness_names[aggressiveness_index]

                player.send_message("§a§l✓ Smooth Tool Configured!§r")
                player.send_message(f"§7Mode: §f{mode_text}§r")
                player.send_message(f"§7Aggressiveness: §f{aggressiveness_text} ({iterations} iteration{'s' if iterations > 1 else ''})§r")
                player.send_message("§6Right-click to apply smooth at your crosshair!§r")

            except (ValueError, IndexError):
                player.send_message("§cInvalid input! Please check your values.§r")

        form.on_submit = on_submit
        player.send_form(form)

    def apply_smooth_at_crosshair(self, player: "Player") -> None:
        """Apply smooth operation at player's crosshair location."""
        player_uuid = player.unique_id
        
        if player_uuid not in self.smooth_settings:
            player.send_message("§cNo smooth settings configured! Sneak + Right-click with the smooth tool to configure.§r")
            return

        settings = self.smooth_settings[player_uuid]
        
        # Get crosshair target
        target_coords = self._get_crosshair_target(player)
        if not target_coords:
            player.send_message("§cNo target block found!§r")
            return
        
        x, y, z = target_coords
        
        try:
            if settings['use_selection']:
                # Use current selection
                if player_uuid not in self.plugin.selections or 'pos1' not in self.plugin.selections[player_uuid] or 'pos2' not in self.plugin.selections[player_uuid]:
                    player.send_message("§cNo selection found! Please set pos1 and pos2 first.§r")
                    return
                player.perform_command(f"smooth {settings['iterations']}")
            else:
                # Use radius at crosshair location
                radius = settings['radius']
                iterations = settings['iterations']
                
                # Create temporary selection at crosshair
                if player_uuid not in self.plugin.selections:
                    self.plugin.selections[player_uuid] = {}
                
                self.plugin.selections[player_uuid]['pos1'] = (x - radius, y - radius, z - radius)
                self.plugin.selections[player_uuid]['pos2'] = (x + radius, y + radius, z + radius)
                
                # Execute smooth command
                player.perform_command(f"smooth {iterations}")
            
            player.send_message(f"§aSmooth applied at your crosshair!§r")
        except Exception as e:
            player.send_message(f"§cError applying smooth: {str(e)}§r")

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

