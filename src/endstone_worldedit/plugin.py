from endstone.plugin import Plugin
from endstone.event import (
    PlayerInteractEvent,
    BlockBreakEvent,
    EventPriority,
    event_handler,
)
from endstone import GameMode
import time
import os
import json
from endstone.command import Command, CommandSender, CommandSenderWrapper
from .commands import preloaded_commands, preloaded_handlers
from .build_areas import BuildAreaManager
from .builder_menu import MenuHandler
from .blueprints import BlueprintManager
from .zones import ZoneManager
from .shape_tool_menu import ShapeToolMenuHandler
from .smooth_tool_menu import SmoothToolMenuHandler


class WorldEditPlugin(Plugin):
    api_version = "0.10"
    commands = preloaded_commands

    def __init__(self):
        super().__init__()
        self.selections = {}
        self.handlers = preloaded_handlers
        self.interaction_cooldown = {}
        self.undo_history = {}
        self.redo_history = {}
        self.clipboard = {}
        self.block_translation_map = {}
        self.particle_toggle = {}  # Stores player UUID -> bool
        self.schematic_previews = {}  # Stores schematic preview data per player UUID
        self.build_area_manager = None  # Initialized in on_load
        self.player_previous_gamemode = {}  # Track player gamemodes for area transitions
        self.menu_handler = None  # Builder menu handler
        self.blueprint_manager = None  # Blueprint manager
        self.zone_manager = None  # Zone manager
        self.smooth_tool_settings = {}  # Stores smooth tool settings per player UUID
        self.shape_tool_handler = ShapeToolMenuHandler(self)
        self.smooth_tool_handler = SmoothToolMenuHandler(self)
        # Removed shape_tool_users - only use interaction events

    def on_load(self):
        self.logger.info("WorldEditPlugin has been loaded!")
        self.load_config()

        # Initialize build area manager
        self.build_area_manager = BuildAreaManager()

        # Initialize blueprint manager
        blueprint_folder = "plugins/WorldEdit/blueprints"
        shared_folder = "plugins/WorldEdit/blueprints/shared"
        self.blueprint_manager = BlueprintManager(blueprint_folder, shared_folder)

        # Initialize zone manager
        self.zone_manager = ZoneManager()

        # Initialize menu handler
        self.menu_handler = MenuHandler(self)

        # Create schematics directory if it doesn't exist
        schematic_path = self.plugin_config.get("schematic-path", "plugins/WorldEdit/schematics")
        if not os.path.exists(schematic_path):
            os.makedirs(schematic_path)

    def load_config(self):
        config_path = "plugins/WorldEdit/config.json"
        default_block_translation_map = {
            "cobblestone_stairs": "stone_stairs",
            "rooted_dirt": "dirt",
            "flowering_azalea_leaves": "azalea_leaves_flowered",
            "slime_block": "slime",
            "sugar_cane": "reeds",
            "small_dripleaf": "small_dripleaf_block",
            "magma_block": "magma",
            "lily_pad": "waterlily",
            "dead_bush": "deadbush",
            "snow_block": "snow",
            "dirt_path": "grass_path",
            "jack_o_lantern": "lit_pumpkin",
            "melon": "melon_block",
            "end_stone_bricks": "end_bricks",
            "end_stone_brick_stairs": "end_brick_stairs",
            "prismarine_brick_stairs": "prismarine_stairs",
            "nether_bricks": "nether_brick",
            "bricks": "brick_block",
            "red_nether_bricks": "red_nether_brick",
            "note_block": "noteblock",
            "cobweb": "web",
            "nether_quartz_ore": "quartz_ore",
            "waxed_copper_block": "copper_block",
            "repeater": "unpowered_repeater",
            "comparator": "unpowered_comparator",
            "powered_rail": "golden_rail",
            "beetroots": "beetroot",
            "oak_door": "wooden_door",
            "oak_trapdoor": "trapdoor",
            "oak_fence": "fence",
            "oak_fence_gate": "fence_gate",
            "oak_button": "wooden_button",
            "oak_pressure_plate": "wooden_pressure_plate",
            "oak_sign": "standing_sign",
            "oak_wall_sign": "wall_sign",
            "warped_sign": "standing_sign",
            "warped_wall_sign": "wall_sign",
            "crimson_sign": "standing_sign",
            "crimson_wall_sign": "wall_sign",
            "bamboo_sign": "standing_sign",
            "bamboo_wall_sign": "wall_sign",
            "cherry_sign": "standing_sign",
            "cherry_wall_sign": "wall_sign",
            "mangrove_sign": "standing_sign",
            "mangrove_wall_sign": "wall_sign",
            "jungle_sign": "standing_sign",
            "jungle_wall_sign": "wall_sign",
            "acacia_sign": "standing_sign",
            "acacia_wall_sign": "wall_sign",
            "dark_oak_sign": "standing_sign",
            "dark_oak_wall_sign": "wall_sign",
            "birch_sign": "standing_sign",
            "birch_wall_sign": "wall_sign",
            "spruce_sign": "standing_sign",
            "spruce_wall_sign": "wall_sign",
            "oak_wall_hanging_sign": "wall_sign",
            "terracotta": "hardened_clay",
            "light_gray_glazed_terracotta": "light_gray_concrete",
            "dark_oak_standing_sign": "standing_sign",
            "sign": "standing_sign",
        }
        default_config = {
            "async-threshold": 5000,
            "particle-type": "minecraft:endrod",
            "particle-density-step": 5,
            "schematic-path": "plugins/WorldEdit/schematics",
            "block_translation_map": default_block_translation_map,
            "build_areas": {
                "enabled": True,
                "restrict_non_operators": True,
                "auto_creative_mode": True,
                "show_area_messages": True
            }
        }
        
        if not os.path.exists(config_path):
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            self.plugin_config = default_config
            with open(config_path, 'w') as f:
                json.dump(self.plugin_config, f, indent=4)
        else:
            with open(config_path, 'r') as f:
                self.plugin_config = json.load(f)
        
        self.block_translation_map = self.plugin_config.get("block_translation_map", {})

    def on_enable(self):
        self.logger.info("WorldEditPlugin has been enabled!")
        self.register_events(self)
        self.tasks = {}
        self.silent_sender = CommandSenderWrapper(self.server.command_sender, on_message=lambda msg: None)
        self.server.scheduler.run_task(self, self.run_tasks, delay=1, period=1)
        self.server.scheduler.run_task(self, self.show_selection_particles, delay=20, period=20)  # Every second
        self.server.scheduler.run_task(self, self.show_schematic_preview_particles, delay=20, period=20)  # Every second
        self.server.scheduler.run_task(self, self.check_build_areas, delay=20, period=20)  # Check build areas every second
        self.player_last_area = {}  # Track which area each player was last in
        # Removed shape tool detection task - only use interaction events

    def show_selection_particles(self):
        for player_uuid, selection in self.selections.items():
            # Check if particles are enabled for this player
            if not self.particle_toggle.get(player_uuid, True):
                continue

            if "pos1" in selection and "pos2" in selection:
                player = self.server.get_player(player_uuid)
                if player:
                    pos1 = selection["pos1"]
                    pos2 = selection["pos2"]
                    min_x, max_x = min(pos1[0], pos2[0]), max(pos1[0], pos2[0])
                    min_y, max_y = min(pos1[1], pos2[1]), max(pos1[1], pos2[1])
                    min_z, max_z = min(pos1[2], pos2[2]), max(pos1[2], pos2[2])

                    # Draw a grid of particles along the edges, executed by the player
                    step = self.plugin_config["particle-density-step"]
                    particle_type = self.plugin_config["particle-type"]
                    # Draw a grid of particles along the edges, executed by the player
                    step = self.plugin_config["particle-density-step"]
                    particle_type = self.plugin_config["particle-type"]
                    player_name = player.name
                    
                    def run_particle_command(x, y, z):
                        command = f"execute as {player.name} at @s run particle {particle_type} {x} {y} {z}"
                        self.server.dispatch_command(self.silent_sender, command)

                    for x in range(int(min_x), int(max_x) + 1, step):
                        run_particle_command(x, min_y, min_z)
                        run_particle_command(x, max_y, min_z)
                        run_particle_command(x, min_y, max_z)
                        run_particle_command(x, max_y, max_z)
                    for y in range(int(min_y), int(max_y) + 1, step):
                        run_particle_command(min_x, y, min_z)
                        run_particle_command(max_x, y, min_z)
                        run_particle_command(min_x, y, max_z)
                        run_particle_command(max_x, y, max_z)
                    for z in range(int(min_z), int(max_z) + 1, step):
                        run_particle_command(min_x, min_y, z)
                        run_particle_command(max_x, min_y, z)
                        run_particle_command(min_x, max_y, z)
                        run_particle_command(max_x, max_y, z)

    def show_schematic_preview_particles(self):
        """Show particle outline for schematic previews."""
        for player_uuid, preview_data in list(self.schematic_previews.items()):
            # Check if particles are enabled for this player
            if not self.particle_toggle.get(player_uuid, True):
                continue

            player = self.server.get_player(player_uuid)
            if player:
                # Update preview position to follow player
                width, height, length = preview_data['dimensions']
                player_location = player.location

                min_x = int(player_location.x)
                min_y = int(player_location.y)
                min_z = int(player_location.z)
                max_x = min_x + width - 1
                max_y = min_y + height - 1
                max_z = min_z + length - 1

                # Update stored preview data
                preview_data['min_pos'] = (min_x, min_y, min_z)
                preview_data['max_pos'] = (max_x, max_y, max_z)

                # Use different particle for preview (yellow/orange flame)
                step = self.plugin_config["particle-density-step"]
                # Use basic_flame_particle for yellow/orange color (different from selection)
                particle_type = "minecraft:basic_flame_particle"

                def run_particle_command(x, y, z):
                    # Use same format as selection particles
                    command = f"execute as {player.name} at @s run particle {particle_type} {x} {y} {z}"
                    self.server.dispatch_command(self.silent_sender, command)

                # Draw edges of the preview box
                for x in range(int(min_x), int(max_x) + 1, step):
                    run_particle_command(x, min_y, min_z)
                    run_particle_command(x, max_y, min_z)
                    run_particle_command(x, min_y, max_z)
                    run_particle_command(x, max_y, max_z)
                for y in range(int(min_y), int(max_y) + 1, step):
                    run_particle_command(min_x, y, min_z)
                    run_particle_command(max_x, y, min_z)
                    run_particle_command(min_x, y, max_z)
                    run_particle_command(max_x, y, max_z)
                for z in range(int(min_z), int(max_z) + 1, step):
                    run_particle_command(min_x, min_y, z)
                    run_particle_command(max_x, min_y, z)
                    run_particle_command(min_x, max_y, z)
                    run_particle_command(max_x, max_y, z)

    def run_tasks(self):
        for player_uuid, task_info in list(self.tasks.items()):
            dimension = task_info["dimension"]
            blocks_to_change = task_info["blocks"]
            
            # Process a chunk of blocks each tick
            chunk_size = self.plugin_config["async-threshold"]
            for _ in range(chunk_size):
                if not blocks_to_change:
                    player = self.server.get_player(player_uuid)
                    if player:
                        player.send_message("Async operation complete.")
                    del self.tasks[player_uuid]
                    break
                
                # Unpack data, now including the data value
                try:
                    if not blocks_to_change:
                        break
                    block_data = blocks_to_change.pop(0)
                    
                    # Handle both 4-value and 5-value tuples for compatibility
                    if len(block_data) == 5:
                        x, y, z, block_type, data_value = block_data
                    else:
                        x, y, z, block_type = block_data
                        data_value = None

                    block = dimension.get_block_at(x, y, z)
                    block.set_type(block_type)
                    if data_value is not None:
                        block.set_data(data_value) # Assuming data_value is the saved block data
                except RuntimeError as e:
                    self.logger.error(f"Skipping block '{block_type}' for player {player_uuid}: {e}")
                    player = self.server.get_player(player_uuid)
                    if player:
                        player.send_message(f"§cSkipped block: {block_type} ({e})§r")
                    continue  # Skip to the next block

    def check_build_areas(self):
        """Check player positions and manage creative mode in build areas"""
        if not self.plugin_config.get("build_areas", {}).get("enabled", True):
            return

        if not self.plugin_config.get("build_areas", {}).get("auto_creative_mode", True):
            return

        for player in self.server.online_players:
            # Skip operators
            if player.is_op:
                continue

            player_uuid = player.unique_id
            player_name = player.name
            location = player.location
            world = player.dimension.name

            # Get areas at current location
            current_areas = self.build_area_manager.get_areas_at_location(
                world, location.x, location.y, location.z
            )

            # Filter to areas where player is authorized
            authorized_areas = [area for area in current_areas if area.has_builder(player_name)]

            # Determine if player should be in creative mode
            should_be_creative = any(area.creative_mode for area in authorized_areas)

            # Get last known area
            last_area_name = self.player_last_area.get(player_uuid)
            current_area_name = authorized_areas[0].name if authorized_areas else None

            # Check if player entered or left a build area
            if last_area_name != current_area_name:
                self.player_last_area[player_uuid] = current_area_name

                if current_area_name:
                    # Player entered a build area
                    area = authorized_areas[0]
                    if self.plugin_config.get("build_areas", {}).get("show_area_messages", True):
                        player.send_message(f"§aEntered build area: §e{area.name}§r")
                        if area.creative_mode:
                            player.send_message("§7Creative mode enabled§r")

                    # Save current gamemode if not already saved
                    if player_uuid not in self.player_previous_gamemode:
                        self.player_previous_gamemode[player_uuid] = player.game_mode

                    # Set creative mode if area requires it
                    if area.creative_mode and player.game_mode != GameMode.CREATIVE:
                        player.game_mode = GameMode.CREATIVE

                elif last_area_name:
                    # Player left a build area
                    if self.plugin_config.get("build_areas", {}).get("show_area_messages", True):
                        player.send_message(f"§7Left build area: §e{last_area_name}§r")

                    # Restore previous gamemode
                    if player_uuid in self.player_previous_gamemode:
                        previous_mode = self.player_previous_gamemode[player_uuid]
                        if player.game_mode != previous_mode:
                            player.game_mode = previous_mode
                            if self.plugin_config.get("build_areas", {}).get("show_area_messages", True):
                                player.send_message("§7Gamemode restored§r")
                        del self.player_previous_gamemode[player_uuid]

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        # Debug logging for all commands
        self.logger.info(f"[COMMAND DEBUG] Command: {command.name}, Args: {args}, Sender: {sender.name}")

        if command.name in self.handlers:
            handler = self.handlers[command.name]
            return handler(self, sender, args)
        else:
            self.logger.warning(f"[COMMAND DEBUG] No handler found for command: {command.name}")
        return False

    @event_handler(priority=EventPriority.HIGH)
    def on_block_break(self, event: BlockBreakEvent):
        """Handle block break events for wand tool only."""
        player = event.player
        item = player.inventory.item_in_main_hand
        if item is not None and item.type == "minecraft:wooden_axe":
            # Wooden axe - wand tool (left-click for pos1)
            event.cancel()
            player_uuid = player.unique_id
            if player_uuid not in self.selections:
                self.selections[player_uuid] = {}
            block = event.block
            self.selections[player_uuid]["pos1"] = (block.x, block.y, block.z)
            player.send_message(f"§aPosition 1 set to ({block.x}, {block.y}, {block.z}).§r")

    @event_handler(priority=EventPriority.HIGH)
    def on_player_interact(self, event: PlayerInteractEvent):
        """Handle player interact events for tools."""
        player = event.player
        player_uuid = player.unique_id
        current_time = time.time()

        # Check cooldown
        last_interact_time = self.interaction_cooldown.get(player_uuid, 0)
        if current_time - last_interact_time < 0.1:  # 100ms cooldown
            return

        # Only handle right-click events
        if event.action.name == "RIGHT_CLICK_BLOCK":
            item = player.inventory.item_in_main_hand
            if item is not None and item.type == "minecraft:wooden_shovel":
                # Wooden shovel - shape tool
                event.cancel()
                self.interaction_cooldown[player_uuid] = current_time

                if player.is_sneaking:
                    # Sneaking + right-click = Configure shape
                    if self.shape_tool_handler:
                        self.shape_tool_handler.show_shape_selection_menu(player)
                else:
                    # Standing + right-click = Spawn shape
                    if self.shape_tool_handler:
                        self.shape_tool_handler.spawn_shape_at_crosshair(player)
            elif item is not None and item.type == "minecraft:wooden_axe":
                # Wooden axe - wand tool (right-click for pos2)
                self.interaction_cooldown[player_uuid] = current_time
                if player_uuid not in self.selections:
                    self.selections[player_uuid] = {}
                block = event.block
                if block:  # Only if clicking on a block
                    self.selections[player_uuid]["pos2"] = (block.x, block.y, block.z)
                    player.send_message(f"§aPosition 2 set to ({block.x}, {block.y}, {block.z}).§r")
            elif item is not None and item.type == "minecraft:wooden_hoe":
                # Wooden hoe - smooth tool
                event.cancel()
                self.interaction_cooldown[player_uuid] = current_time

                if player.is_sneaking:
                    # Sneaking + right-click = Configure smooth
                    if self.smooth_tool_handler:
                        self.smooth_tool_handler.show_smooth_config_menu(player)
                else:
                    # Standing + right-click = Apply smooth at crosshair
                    if self.smooth_tool_handler:
                        self.smooth_tool_handler.apply_smooth_at_crosshair(player)

    def _check_shape_tool_usage(self):
        """Check for shape tool usage every tick."""
        for player in self.server.online_players:
            player_uuid = player.unique_id
            item = player.inventory.item_in_main_hand
            
            if item is not None and item.type == "minecraft:wooden_shovel":
                # Player is holding shape tool
                if player_uuid not in self.shape_tool_users:
                    self.shape_tool_users[player_uuid] = {
                        'last_sneak': False,
                        'last_jump': False,
                        'cooldown': 0
                    }
                
                # Check if player is sneaking (shift) to trigger shape spawn
                current_sneak = player.is_sneaking
                user_data = self.shape_tool_users[player_uuid]
                
                # Detect sneak press (not held)
                if current_sneak and not user_data['last_sneak']:
                    current_time = time.time()
                    if current_time - user_data['cooldown'] > 1.0:  # 1 second cooldown
                        user_data['cooldown'] = current_time
                        if self.shape_tool_handler:
                            self.shape_tool_handler.spawn_shape_at_crosshair(player)
                
                user_data['last_sneak'] = current_sneak
            else:
                # Player not holding shape tool, remove from tracking
                if player_uuid in self.shape_tool_users:
                    del self.shape_tool_users[player_uuid]
