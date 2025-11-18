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
- [Configuration](#-configuration)
- [Commands](#-commands)
- [Permissions](#-permissions)
- [Usage Examples](#-usage-examples)
- [Changelog](#-changelog)

---

## ✨ Features

### 🎨 Core WorldEdit Functionality
- **Selection Tools** - Wand-based or command-based region selection
- **Block Operations** - Set, replace, walls, overlay, and more
- **Clipboard System** - Copy, cut, and paste structures
- **History Management** - Unlimited undo/redo support
- **Shape Generation** - Create spheres, cylinders (solid & hollow)
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
| `/pos1` | - | Set position 1 to your location | `worldedit.command.pos1` |
| `/pos2` | - | Set position 2 to your location | `worldedit.command.pos2` |
| `/sel` | - | Show selection info | `worldedit.command.sel` |
| `/sel clear` | `/deselect` | Clear current selection | `worldedit.command.sel` |
| `/sel toggle` | - | Toggle selection particles | `worldedit.command.sel` |

**Wand Usage:**
- **Left-Click** a block → Set Position 1
- **Right-Click** a block → Set Position 2

### ✏️ Editing Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/set <block>` | Fill selection with a block | `worldedit.command.set` |
| `/replace <from> <to>` | Replace blocks in selection | `worldedit.command.replace` |
| `/walls <block>` | Create walls around selection | `worldedit.command.walls` |
| `/overlay <block>` | Overlay blocks on top surface | `worldedit.command.overlay` |

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
    ├── worldedit.command.pos1
    ├── worldedit.command.pos2
    ├── worldedit.command.sel
    ├── worldedit.command.set
    ├── worldedit.command.replace
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

### Version 3.0.0 - Builder's Edition (Current)

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

**📝 Documentation**
- 📚 Comprehensive README with examples and guides
- 📚 Complete command reference with permissions
- 📚 Configuration documentation
- 📚 Usage examples for common scenarios

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

