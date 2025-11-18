# 🏗️ WorldEdit for Endstone - Builder's Edition

<div align="center">

**A comprehensive WorldEdit plugin for Endstone with Builder's Menu, Build Areas, Blueprints, Zones, and Advanced Editing Tools**

[![Version](https://img.shields.io/badge/version-3.1.0-blue.svg)](https://github.com/iciency/WorldEdit)
[![Endstone](https://img.shields.io/badge/endstone-0.10+-green.svg)](https://github.com/EndstoneMC/endstone)
[![Python](https://img.shields.io/badge/python-3.9+-yellow.svg)](https://www.python.org/)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [How To Use](#-how-to-use)
  - [Tools Guide](#-tools-guide)
  - [Menu System](#-menu-system)
  - [Commands Reference](#-commands-reference)
- [Configuration](#-configuration)
- [Commands](#-commands)
- [Permissions](#-permissions)
- [Usage Examples](#-usage-examples)
- [Changelog](#-changelog)

---

## ✨ Features

### 🎨 Core WorldEdit Functionality
- **Selection Tools** - Wand-based or command-based region selection
- **Smooth Tool** - Terrain smoothing with wooden hoe (configurable aggressiveness)
- **Block Operations** - Set, replace, walls, overlay, and more
- **Clipboard System** - Copy, cut, and paste structures
- **History Management** - Unlimited undo/redo support
- **Shape Generation** - Spheres, cylinders, pyramids, squares (solid & hollow)
- **Schematic Support** - Save/load `.schem` files with Java Edition compatibility
- **Async Operations** - Large edits processed in chunks to prevent lag

### 🏗️ Builder's Menu System (NEW!)
- **Interactive Menu** - `/builder` or `/bmenu` shows status, areas, and commands at a glance
- **Area Discovery** - `/myareas` lists all accessible build zones
- **Real-time Info** - `/areainfo` displays current location status
- **UI-Based Operations** - Easy-to-use forms for selection, clipboard, and paste operations
- **Quick Access** - All WorldEdit features accessible through intuitive menus

### 🔐 Build Area Management (NEW!)
- **Designated Build Zones** - Operators create cuboid regions for builders
- **Permission Control** - Non-operators restricted to assigned areas
- **Auto Creative Mode** - Automatic gamemode switching on entry/exit
- **Multi-Builder Support** - Assign multiple players per area
- **Area Notifications** - Real-time messages when crossing boundaries
- **Teleportation** - Quick travel to managed build areas

### 📘 Blueprint System (NEW!)
- **Save & Load** - Save clipboard contents as reusable blueprints
- **Personal Library** - Each player has their own blueprint collection
- **Shared Blueprints** - Share blueprints with other players
- **Compression** - Efficient storage with palette mapping and RLE compression
- **Metadata** - Track author, creation date, and descriptions

### 🌍 Builder Zones (NEW!)
- **Temporary Zones** - Create time-limited build areas
- **Zone Management** - Operators can create and manage builder zones
- **Flexible Sizing** - Configurable radius and duration
- **Zone Integration** - Works seamlessly with build area system

---

## 📦 Installation

### Prerequisites
- Endstone server (version 0.5.0 or higher with Form API support)
- Python 3.9+
- `nbtlib` package (auto-installed with plugin)

### Steps

1. **Build the Plugin**
   ```bash
   pip install build
   python -m build
   ```
   This creates `dist/endstone_worldedit-3.1.0-py3-none-any.whl`

2. **Install to Server**
   ```bash
   # Copy the .whl file to your server's plugins folder
   cp dist/endstone_worldedit-3.1.0-py3-none-any.whl /path/to/server/plugins/
   ```

3. **Restart Server**
   ```bash
   # Start or restart your Endstone server
   # The plugin will auto-generate config files on first load
   ```

4. **Verify Installation**
   ```
   Check server logs for: "WorldEditPlugin has been enabled!"
   ```

---

## 🚀 Quick Start

### For Server Operators

**Set up your first build area:**

```bash
# 1. Get the selection wand
/wand

# 2. Select the area (left-click pos1, right-click pos2)
#    Or use commands:
/pos1
/pos2

# 3. Create the build area
/area create creative_zone

# 4. Add builders
/area addbuilder creative_zone Steve
/area addbuilder creative_zone Alex

# 5. Done! Builders can now use WorldEdit in this area
```

### For Builders

**Start building in your assigned areas:**

```bash
# 1. Check where you can build
/myareas

# 2. Open the builder's menu
/bmenu

# 3. Get your wand
/wand

# 4. Go to your build area (you'll auto-switch to creative mode)

# 5. Make a selection and start editing!
/pos1
/pos2
/set stone
```

---

## 📖 How To Use

This section provides comprehensive guides for using all the tools, menus, and commands in WorldEdit.

### 🔨 Tools Guide

WorldEdit provides two main tools that make editing easier and more intuitive.

#### **Selection Wand (Wooden Axe)**

The selection wand is used to select regions for editing.

**How to get it:**
```bash
/wand          # Get the selection wand
# OR
/w             # Short alias
```

**How to use it:**
- **Left-Click** a block → Sets Position 1 (first corner)
- **Right-Click** a block → Sets Position 2 (opposite corner)
- You'll see particles showing your selection
- The selection forms a cuboid (rectangular box) between the two points

**Example workflow:**
```bash
1. Type /wand to get the wooden axe
2. Left-click a block at one corner of your desired area
   → Message: "Position 1 set to (100, 64, 200)"
3. Right-click a block at the opposite corner
   → Message: "Position 2 set to (150, 80, 250)"
4. You now have a 51x17x51 block selection!
5. Use any editing command: /set stone, /copy, etc.
```

**Tips:**
- You can also set positions with commands: `/pos1` and `/pos2` (uses your current location)
- Toggle selection particles on/off: `/sel toggle`
- Clear your selection: `/sel clear`
- Check selection info: `/sel`

---

#### **Smooth Tool (Wooden Hoe)**

The smooth tool is used to smooth terrain and remove rough edges.

**How to get it:**
```bash
/smoothtool    # Get the smooth tool
# OR
/st            # Short alias
```

**How to use it:**

**Step 1: Configure (Right-Click)**
1. Hold the wooden hoe
2. Right-click anywhere
3. Configuration menu opens with these options:
   - **Radius** (1-20): Area size around you to smooth
   - **Aggressiveness**: How strong the smoothing is
     - Gentle (1 iteration) - Very subtle
     - Light (2 iterations) - Slight smoothing
     - Medium (3 iterations) - Balanced ⭐ Recommended
     - Strong (5 iterations) - Heavy smoothing
     - Very Strong (7 iterations) - Very smooth
     - Extreme (10 iterations) - Nearly flat
   - **Use Current Selection**: Toggle to use wand selection instead of radius

4. Submit your settings
5. You'll see: "✓ Smooth Tool Configured!"

**Step 2: Execute (Left-Click)**
1. Hold the wooden hoe
2. Left-click anywhere (or on a block)
3. Terrain smooths instantly with your saved settings!
4. No menu popup - just smooth!

**Example workflow:**
```bash
# First time setup
1. /smoothtool                    # Get the tool
2. Right-click                    # Configure
   - Radius: 10
   - Aggressiveness: Medium
   - Use Selection: OFF
3. Submit                         # Settings saved

# Now use it repeatedly
4. Left-click at rough terrain    # Smooths 10 block radius
5. Move to another spot
6. Left-click again               # Smooths again (no menu!)
7. Keep left-clicking to smooth more areas!

# Change settings anytime
8. Right-click                    # Menu shows current settings
9. Change to: Radius 5, Strong
10. Submit
11. Left-click                    # Uses new settings
```

**Two modes:**

**Radius Mode** (Default):
- Creates a cube around you based on radius
- Perfect for smoothing terrain as you walk
- Quick and easy

**Selection Mode**:
- Uses your wand selection (pos1/pos2)
- Perfect for smoothing specific areas
- More precise control

**Tips:**
- Start with "Medium" aggressiveness and adjust from there
- Larger radius = more area smoothed at once
- You can undo smoothing with `/undo`
- Settings are saved per player - each player has their own configuration

---

### 📱 Menu System

WorldEdit includes an interactive menu system for easy access to all features.

#### **Main Builder Menu**

**How to open:**
```bash
/builder       # Main command
# OR
/bmenu         # Alternative
# OR
/b             # Short alias
```

**What you'll see:**

The main menu shows:
- Your current build area (if you're in one)
- Your selection status (pos1/pos2)
- Quick access buttons to all features

**Menu Categories:**

1. **Selection Tools**
   - Set Position 1 (at your location)
   - Set Position 2 (at your location)
   - Get Selection Wand (wooden axe)
   - Get Smooth Tool (wooden hoe)
   - Clear Selection

2. **Clipboard**
   - Copy (copy selection to clipboard)
   - Cut (cut selection to clipboard)
   - Paste (paste clipboard at your location)
   - Advanced Paste (with rotation, flip, offset options)

3. **Editing**
   - Set Blocks (fill selection with a block)
   - Replace Blocks (replace one block type with another)
   - Walls (create walls around selection)
   - Overlay (place blocks on top surface)

4. **Transform**
   - Rotate 90° (rotate selection clockwise)
   - Rotate 180° (rotate selection 180 degrees)
   - Rotate 270° (rotate selection counter-clockwise)
   - Flip X (flip selection left/right)
   - Flip Y (flip selection up/down)
   - Flip Z (flip selection forward/backward)

5. **Shapes**
   - Sphere (solid sphere)
   - Hollow Sphere
   - Cylinder (solid cylinder)
   - Hollow Cylinder
   - Square (solid rectangular prism)
   - Hollow Square (hollow box)
   - Pyramid (solid pyramid)
   - Hollow Pyramid

6. **Schematics**
   - Save Schematic (save selection to file)
   - Load & Place Schematic (load and paste)
   - List Schematics (view all saved schematics)

7. **Build Areas** (Operators only)
   - Create Build Area (from coordinates)
   - Add Builder to Area (grant access)
   - List Build Areas
   - Manage Areas

8. **Undo/Redo**
   - Undo Last Action
   - Redo Last Action
   - Shows number of available undo/redo actions

**Example menu workflow:**
```bash
1. /builder                       # Open menu
2. Click "Selection Tools"        # Opens selection submenu
3. Click "Get Selection Wand"     # Receive wooden axe
4. Close menu and select area with wand
5. /builder                       # Open menu again
6. Click "Editing"                # Opens editing submenu
7. Click "Set Blocks"             # Opens form
8. Enter "stone"                  # Block type
9. Submit                         # Selection fills with stone!
```

---

### 📝 Commands Reference

This section provides detailed command usage with examples.

#### **Selection Commands**

**Set positions manually:**
```bash
/pos1          # Set position 1 at your current location
/pos2          # Set position 2 at your current location

# Example:
# Stand at one corner
/pos1          # → "Position 1 set to (100, 64, 200)"
# Walk to opposite corner
/pos2          # → "Position 2 set to (150, 80, 250)"
```

**Check selection:**
```bash
/sel           # Show selection info
# Output: "Selection: 51x17x51 (44,217 blocks)"

/sel clear     # Clear your selection
/sel toggle    # Toggle selection particles on/off
```

---

#### **Editing Commands**

**Fill selection with blocks:**
```bash
/set <block>

# Examples:
/set stone                    # Fill with stone
/set glass                    # Fill with glass
/set minecraft:oak_planks     # Full block ID
```

**Replace blocks:**
```bash
/replace <from_block> <to_block>

# Examples:
/replace dirt grass           # Replace all dirt with grass
/replace stone cobblestone    # Replace stone with cobblestone
/replace air water            # Fill air spaces with water
```

**Create walls:**
```bash
/walls <block>

# Example:
/walls stone_bricks           # Create walls around selection
# Only places blocks on the outer edges
```

**Overlay blocks:**
```bash
/overlay <block>

# Example:
/overlay grass                # Place grass on top surface
# Only affects the top layer of blocks
```

**Smooth terrain:**
```bash
/smooth [iterations]

# Examples:
/smooth                       # Smooth once (gentle)
/smooth 3                     # Smooth 3 times (medium)
/smooth 10                    # Smooth 10 times (extreme)

# Note: Requires a selection first
```

---

#### **Transform Commands**

**Rotate selection:**
```bash
/rotate <degrees>

# Examples:
/rotate 90                    # Rotate 90° clockwise
/rotate 180                   # Rotate 180°
/rotate 270                   # Rotate 270° clockwise (90° counter-clockwise)
/rotate -90                   # Same as 270°

# Note: Rotates around Y-axis (vertical)
# Selection must be made first
```

**Flip selection:**
```bash
/flip [x|y|z]

# Examples:
/flip x                       # Flip left/right
/flip y                       # Flip up/down
/flip z                       # Flip forward/backward
/flip                         # Flip along Z-axis (default)

# Note: Flips the selection in place
# Selection must be made first
```

**Example workflow:**
```bash
1. Select a structure with wand
2. /rotate 90                 # Rotate it 90 degrees
3. /flip x                    # Flip it horizontally
4. /undo                      # Oops, undo the flip
5. /flip z                    # Flip it the other way
```

---

#### **Clipboard Commands**

**Copy selection:**
```bash
/copy

# Example workflow:
1. Select area with wand
2. /copy                      # → "Copied 1,234 blocks"
3. Walk to new location
4. /paste                     # Paste it there
```

**Cut selection:**
```bash
/cut

# Example:
1. Select area with wand
2. /cut                       # → "Cut 1,234 blocks" (area becomes air)
3. Walk to new location
4. /paste                     # Paste it there
```

**Paste clipboard:**
```bash
/paste

# Example:
1. /copy or /cut first
2. Walk to where you want to paste
3. /paste                     # Pastes at your location
```

---

#### **Shape Commands**

**Create spheres:**
```bash
/sphere <block> <radius>
/hsphere <block> <radius>     # Hollow version

# Examples:
/sphere glass 10              # 10-block radius glass sphere
/hsphere stone 15             # 15-block radius hollow stone sphere
```

**Create cylinders:**
```bash
/cyl <block> <radius> [height]
/hcyl <block> <radius> [height]   # Hollow version

# Examples:
/cyl stone 5                  # 5-block radius cylinder (default height)
/cyl stone 5 10               # 5-block radius, 10 blocks tall
/hcyl glass 8 20              # Hollow glass cylinder
```

**Create pyramids:**
```bash
/pyramid <block> <size>
/hpyramid <block> <size>      # Hollow version

# Examples:
/pyramid sandstone 10         # 10-block tall solid pyramid
/hpyramid glass 15            # 15-block tall hollow pyramid
```

**Create squares (rectangular prisms):**
- Use the menu: `/builder` → Shapes → Square
- Configure width, height, length
- Choose solid or hollow

---

#### **Schematic Commands**

**Save selection as schematic:**
```bash
/schem save <name>

# Example:
1. Select your build with wand
2. /schem save my_house       # Saves to plugins/WorldEdit/schematics/my_house.schem
```

**Load schematic:**
```bash
/schem load <name>

# Example:
/schem load my_house          # Loads into clipboard
/paste                        # Paste it
```

**List schematics:**
```bash
/schem list

# Output:
# Available schematics:
#   - my_house.schem
#   - tower.schem
#   - bridge.schem
```

---

#### **History Commands**

**Undo/Redo:**
```bash
/undo          # Undo last action
/redo          # Redo last undone action

# Example:
/set stone     # Fill selection with stone
/undo          # Oops! Undo it
/redo          # Actually, redo it
/undo          # Changed my mind again
```

---

#### **Build Area Commands (Operators Only)**

**Create build area:**
```bash
# Method 1: Using menu (recommended)
/builder → Build Areas → Create Build Area
# Enter coordinates for corner 1 and corner 2

# Method 2: Using selection
1. Select area with wand
2. /area create <name>

# Example:
/area create spawn_plaza
```

**Manage builders:**
```bash
/area addbuilder <area_name> <player_name>
/area removebuilder <area_name> <player_name>

# Examples:
/area addbuilder spawn_plaza Steve
/area addbuilder spawn_plaza Alex
/area removebuilder spawn_plaza Steve
```

**List and info:**
```bash
/area list                    # List all build areas
/area info <name>             # Show area details
/myareas                      # Show areas you can access (all players)
/areainfo                     # Show current area info (all players)
```

**Teleport:**
```bash
/area tp <name>

# Example:
/area tp spawn_plaza          # Teleport to the area
```

---

## ⚙️ Configuration

The plugin creates `plugins/WorldEdit/config.json` on first run:

```json
{
    "async-threshold": 5000,
    "particle-type": "minecraft:endrod",
    "particle-density-step": 5,
    "schematic-path": "plugins/WorldEdit/schematics",
    "block_translation_map": {
        "cobblestone_stairs": "stone_stairs",
        "rooted_dirt": "dirt",
        "sugar_cane": "reeds"
    },
    "build_areas": {
        "enabled": true,
        "restrict_non_operators": true,
        "auto_creative_mode": true,
        "show_area_messages": true
    }
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `async-threshold` | int | 5000 | Block count threshold for async processing |
| `particle-type` | string | `minecraft:endrod` | Particle for selection visualization |
| `particle-density-step` | int | 5 | Distance between selection particles |
| `schematic-path` | string | `plugins/WorldEdit/schematics` | Schematic storage directory |
| `block_translation_map` | object | {...} | Java→Bedrock block name translations |

### Build Area Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | true | Enable/disable build area system |
| `restrict_non_operators` | boolean | true | Restrict non-ops to assigned areas only |
| `auto_creative_mode` | boolean | true | Auto-switch to creative in build areas |
| `show_area_messages` | boolean | true | Show entry/exit notifications |

---

## 📝 Commands

### 🔧 Selection Commands

| Command | Aliases | Description | Permission |
|---------|---------|-------------|------------|
| `/wand` | `/w` | Get the selection wand (wooden axe) | `worldedit.command.wand` |
| `/smoothtool` | `/st` | Get the smooth tool (wooden hoe) | `worldedit.command.smoothtool` |
| `/pos1` | - | Set position 1 to your location | `worldedit.command.pos1` |
| `/pos2` | - | Set position 2 to your location | `worldedit.command.pos2` |
| `/sel` | - | Show selection info | `worldedit.command.sel` |
| `/sel clear` | `/deselect` | Clear current selection | `worldedit.command.sel` |
| `/sel toggle` | - | Toggle selection particles | `worldedit.command.sel` |

**Wand Usage:**
- **Left-Click** a block → Set Position 1
- **Right-Click** a block → Set Position 2

**Smooth Tool Usage:**
- **Right-Click** → Configure settings (radius, aggressiveness)
- **Left-Click** → Execute smooth with saved settings

### ✏️ Editing Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/set <block>` | Fill selection with a block | `worldedit.command.set` |
| `/replace <from> <to>` | Replace blocks in selection | `worldedit.command.replace` |
| `/walls <block>` | Create walls around selection | `worldedit.command.walls` |
| `/overlay <block>` | Overlay blocks on top surface | `worldedit.command.overlay` |
| `/smooth [iterations]` | Smooth terrain in selection | `worldedit.command.smooth` |

### 🔄 Transform Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/rotate <degrees>` | Rotate selection around Y-axis (90, 180, 270) | `worldedit.command.rotate` |
| `/flip [x\|y\|z]` | Flip selection along an axis | `worldedit.command.flip` |

**Transform Notes:**
- Rotation is around the Y-axis (vertical) in 90-degree increments
- Flip axes: X = left/right, Y = up/down, Z = forward/backward
- Both commands modify the selection in place
- Use `/undo` to revert if needed

### 📋 Clipboard Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/copy` | Copy selection to clipboard | `worldedit.command.copy` |
| `/cut` | Cut selection to clipboard | `worldedit.command.cut` |
| `/paste` | Paste clipboard at your location | `worldedit.command.paste` |

### ↩️ History Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/undo` | Undo last action | `worldedit.command.undo` |
| `/redo` | Redo last undone action | `worldedit.command.redo` |

### 🔮 Shape Generation Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/sphere <block> <radius>` | Create solid sphere | `worldedit.command.sphere` |
| `/hsphere <block> <radius>` | Create hollow sphere | `worldedit.command.hsphere` |
| `/cyl <block> <radius> [height]` | Create solid cylinder | `worldedit.command.cyl` |
| `/hcyl <block> <radius> [height]` | Create hollow cylinder | `worldedit.command.hcyl` |
| `/pyramid <block> <size>` | Create solid pyramid | `worldedit.command.pyramid` |
| `/hpyramid <block> <size>` | Create hollow pyramid | `worldedit.command.pyramid` |

**Note:** Squares (rectangular prisms) are available through the menu: `/builder` → Shapes → Square

### 💾 Schematic Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/schem save <name>` | Save selection as schematic | `worldedit.command.schem` |
| `/schem load <name>` | Load schematic at your location | `worldedit.command.schem` |
| `/schem list` | List available schematics | `worldedit.command.schem` |

### 🏗️ Build Area Commands (Operators)

| Command | Description | Permission |
|---------|-------------|------------|
| `/area create <name>` | Create build area from selection | `worldedit.admin.area` |
| `/area delete <name>` | Delete a build area | `worldedit.admin.area` |
| `/area list` | List all build areas | `worldedit.admin.area` |
| `/area info <name>` | Show area details | `worldedit.admin.area` |
| `/area addbuilder <area> <player>` | Grant player access to area | `worldedit.admin.area` |
| `/area removebuilder <area> <player>` | Remove player access | `worldedit.admin.area` |
| `/area tp <name>` | Teleport to build area | `worldedit.admin.area` |

### 👷 Builder Menu Commands

| Command | Aliases | Description | Permission |
|---------|---------|-------------|------------|
| `/builder` | `/b`, `/bmenu`, `/buildermenu` | Open interactive builder's menu | None (all players) |
| `/bmenu` | - | Open interactive builder's menu (legacy) | `worldedit.builder.menu` |
| `/myareas` | - | List your accessible build areas | `worldedit.builder.menu` |
| `/areainfo` | - | Show current area information | `worldedit.builder.menu` |

**Builder Menu Features:**
- **Selection Menu** - Set pos1/pos2 with one click
- **Clipboard Menu** - Copy, cut, paste operations
- **Blueprint Menu** - Save and load blueprints
- **Zone Menu** - View and manage builder zones (operators only)
- **Undo Menu** - Quick undo/redo access

---

## 🔐 Permissions

### Permission Hierarchy

```
worldedit.*                    # All permissions (operators)
├── worldedit.admin.*          # Admin permissions
│   └── worldedit.admin.area   # Build area management
├── worldedit.builder.*        # Builder permissions
│   └── worldedit.builder.menu # Builder menu access
└── worldedit.command.*        # All command permissions
    ├── worldedit.command.wand
    ├── worldedit.command.smoothtool
    ├── worldedit.command.pos1
    ├── worldedit.command.pos2
    ├── worldedit.command.sel
    ├── worldedit.command.set
    ├── worldedit.command.replace
    ├── worldedit.command.smooth
    ├── worldedit.command.rotate
    ├── worldedit.command.flip
    ├── worldedit.command.copy
    ├── worldedit.command.cut
    ├── worldedit.command.paste
    ├── worldedit.command.undo
    ├── worldedit.command.redo
    ├── worldedit.command.walls
    ├── worldedit.command.overlay
    ├── worldedit.command.sphere
    ├── worldedit.command.hsphere
    ├── worldedit.command.cyl
    ├── worldedit.command.hcyl
    ├── worldedit.command.pyramid
    └── worldedit.command.schem
```

### Default Permissions

- **Operators**: All permissions (`worldedit.*`)
- **Non-Operators**: No permissions by default (must be granted individually)

### Recommended Permission Sets

**For Trusted Builders:**
```yaml
permissions:
  - worldedit.builder.menu
  - worldedit.command.wand
  - worldedit.command.pos1
  - worldedit.command.pos2
  - worldedit.command.sel
  - worldedit.command.set
  - worldedit.command.replace
  - worldedit.command.copy
  - worldedit.command.paste
  - worldedit.command.undo
  - worldedit.command.redo
```

**For Advanced Builders:**
```yaml
permissions:
  - worldedit.builder.menu
  - worldedit.command.*  # All editing commands
```


---

## 💡 Usage Examples

### Example 1: Building a House Foundation

```bash
# 1. Get your wand
/wand

# 2. Select the foundation area
# Left-click one corner, right-click opposite corner

# 3. Fill with stone
/set stone

# 4. Create walls (4 blocks high)
/pos1
/pos2 ~0 ~4 ~0
/walls stone_bricks

# 5. Add a floor
/overlay oak_planks
```

### Example 2: Creating a Sphere Monument

```bash
# 1. Stand where you want the center
/sphere glass 10

# 2. Make it hollow
/undo
/hsphere glass 10

# 3. Add a glowing core
/sphere glowstone 3
```

### Example 3: Copying and Pasting a Structure

```bash
# 1. Select the structure
/pos1
/pos2

# 2. Copy it
/copy

# 3. Move to new location
# (walk to where you want to paste)

# 4. Paste it
/paste

# 5. Oops, wrong spot? Undo!
/undo

# 6. Move and paste again
/paste
```

### Example 4: Setting Up a Build Area (Operators)

```bash
# Scenario: Create a creative build zone for your build team

# 1. Select the area boundaries
/pos1
/pos2

# 2. Create the build area
/area create creative_plaza

# 3. Add your builders
/area addbuilder creative_plaza Steve
/area addbuilder creative_plaza Alex
/area addbuilder creative_plaza Notch

# 4. Check the area info
/area info creative_plaza

# 5. Teleport to the area
/area tp creative_plaza

# Now Steve, Alex, and Notch can use WorldEdit in this area!
# They'll automatically switch to creative mode when they enter.
```

### Example 5: Builder Workflow

```bash
# As a builder named Steve:

# 1. Check your assigned areas
/myareas
# Output: You have access to 2 build areas:
#   - creative_plaza (overworld)
#   - spawn_design (overworld)

# 2. Open the builder's menu
/bmenu
# Shows: Current area, selection status, clipboard, commands

# 3. Walk into creative_plaza
# Auto-message: "Entered build area: creative_plaza"
# Auto-message: "Creative mode enabled"

# 4. Start building!
/wand
/pos1
/pos2
/set quartz_block

# 5. Leave the area
# Auto-message: "Left build area: creative_plaza"
# Auto-message: "Gamemode restored"
```

### Example 6: Replacing Blocks in a Region

```bash
# Replace all dirt with grass in your selection
/pos1
/pos2
/replace dirt grass

# Replace all stone variants with smooth stone
/replace stone smooth_stone
/replace cobblestone smooth_stone
/replace stone_bricks smooth_stone
```

### Example 7: Using Schematics

```bash
# Save a building
/pos1
/pos2
/schem save my_house

# List all schematics
/schem list

# Load it somewhere else
# (move to new location)
/schem load my_house
/paste

# The schematic is now in your clipboard!
```

---

## 📊 Changelog

### Version 3.1.0 - Tools & Shapes Update (Current)

**🎉 Major Features**
- ✨ **NEW**: Smooth Tool system with wooden hoe for terrain smoothing
  - Right-click to configure (radius, aggressiveness, selection mode)
  - Left-click to execute smooth with saved settings
  - 6 aggressiveness levels from Gentle to Extreme
  - Per-player settings persistence
- ✨ **NEW**: `/smoothtool` command to get the smooth tool
- ✨ **NEW**: `/smooth [iterations]` command for manual terrain smoothing
- ✨ **NEW**: Transform commands for rotating and flipping selections
  - `/rotate <degrees>` - Rotate selection 90°, 180°, or 270°
  - `/flip [x|y|z]` - Flip selection along any axis
  - Transform menu in builder UI for easy access
- ✨ **NEW**: Pyramid shapes - `/pyramid` and `/hpyramid` commands
- ✨ **NEW**: Square shapes (rectangular prisms) via menu - solid and hollow
- ✨ **NEW**: Interactive menu system completely redesigned
  - 9 main categories: Selection, Clipboard, Editing, Transform, Shapes, Schematics, Build Areas, Undo/Redo
  - Transform menu with rotate and flip operations
  - Advanced paste controls with rotation, flip, and offset
  - Schematic loading with full placement controls
  - Build area creation with coordinate inputs

**🐛 Bug Fixes**
- 🔧 **FIXED**: Selection detection in menu (UUID key mismatch)
- 🔧 **FIXED**: Square shape command syntax errors
- 🔧 **FIXED**: ModalForm content attribute error
- 🔧 **FIXED**: Build area creation now uses coordinate inputs instead of selection

**🔨 Improvements**
- 📈 Smooth tool workflow - configure once, use many times
- 📈 All shape commands now working (spheres, cylinders, pyramids, squares)
- 📈 Enhanced menu system with better organization
- 📈 Improved error messages and user feedback
- 📈 Better tool integration (wand + smooth tool)

**📝 Documentation**
- 📚 Comprehensive "How To Use" section added to README
- 📚 Complete tools guide (Selection Wand & Smooth Tool)
- 📚 Detailed menu system documentation
- 📚 Commands reference with examples
- 📚 Updated permissions list

### Version 3.0.0 - Builder's Edition

**🎉 Major Features**
- ✨ **NEW**: Builder's Menu system with `/bmenu`, `/myareas`, and `/areainfo` commands
- ✨ **NEW**: Build Area Management system for operators (`/area` command suite)
- ✨ **NEW**: Automatic creative mode switching when entering/exiting build areas
- ✨ **NEW**: Permission-based area restrictions for non-operators
- ✨ **NEW**: Real-time area entry/exit notifications
- ✨ **NEW**: Multi-builder support with per-area access control

**🐛 Bug Fixes**
- 🔧 **FIXED**: `ValueError: byte must be in range(0, 256)` when saving schematics with large palettes
- 🔧 **FIXED**: Implemented proper varint encoding for Sponge Schematic v2 format

**🔨 Improvements**
- 📈 Enhanced permission system with granular area-based checks
- 📈 Improved configuration system with build area settings
- 📈 Better error messages directing players to available commands
- 📈 Optimized area checking with periodic position tracking

### Version 2.0.2 - Previous Release

**Features**
- Core WorldEdit functionality (set, replace, copy, paste, etc.)
- Schematic support (save/load `.schem` files)
- Shape generation (spheres, cylinders)
- Undo/redo system
- Selection visualization with particles
- Block translation map for Java Edition compatibility

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue with detailed reproduction steps
2. **Suggest Features**: Share your ideas in the issues section
3. **Submit Pull Requests**: Fork the repo and submit PRs for review
4. **Improve Documentation**: Help make the docs clearer and more comprehensive

### Development Setup

```bash
# Clone the repository
git clone https://github.com/iciency/WorldEdit.git
cd WorldEdit

# Install development dependencies
pip install -e .

# Run tests (if available)
pytest

# Build the plugin
python -m build
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Endstone Team** - For creating the amazing Endstone server platform
- **WorldEdit** - Original inspiration from the Java Edition plugin
- **Contributors** - Everyone who has helped improve this plugin

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/iciency/WorldEdit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/iciency/WorldEdit/discussions)
- **Discord**: Join the Endstone Discord for community support

---

<div align="center">

**Made with ❤️ for the Endstone community**

⭐ Star this repo if you find it useful!

</div>

