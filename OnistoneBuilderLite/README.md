# OnistoneBuilderLite

**A lightweight builder menu plugin for Endstone (Minecraft Bedrock Edition)**

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Endstone](https://img.shields.io/badge/endstone-0.5.0+-green.svg)](https://github.com/EndstoneMC/endstone)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

OnistoneBuilderLite is a pure Python server-side plugin for Minecraft Bedrock Edition servers running Endstone. It provides a comprehensive builder menu system with selection tools, clipboard management, blueprint saving/loading, and builder zones - all without requiring any client-side mods or behavior packs.

---

## ✨ Features

### 🎯 Core Functionality
- **Selection System**: Set positions with commands or wand tool
- **Clipboard Management**: Copy, cut, and paste with ring buffer history
- **Blueprint System**: Save and load builds with compression
- **Builder Zones**: Temporary build areas with permissions and expiry
- **Undo System**: Diff-based undo for paste/cut operations
- **Transform Tools**: Rotate (0°/90°/180°/270°) and flip (X/Y/Z) on paste

### 🎨 User Interface
- **Interactive Menus**: Server-UI based forms (no client mods needed)
- **Main Builder Menu**: Central hub for all builder tools
- **Selection Menu**: Visual selection management
- **Clipboard Browser**: View and manage clipboard history
- **Blueprint Library**: Personal and shared blueprint collections
- **Zone Manager**: Create and manage builder zones

### 🔐 Permission System
- **Granular Permissions**: Fine-grained control over features
- **Zone-Based Access**: Restrict building to designated areas
- **Admin Tools**: Zone management and blueprint moderation
- **Bypass Options**: Allow trusted users to bypass restrictions

---

## 📦 Installation

### Prerequisites
- **Minecraft Bedrock Server** running **Endstone v0.5.0+**
- **Python 3.9+**
- **server-ui 2.1.0-beta** (Python library)

### Steps

1. **Install Dependencies**:
   ```bash
   pip install endstone>=0.5.0 server-ui>=2.1.0b0
   ```

2. **Download Plugin**:
   - Download the `OnistoneBuilderLite` folder
   - Place it in your server's `plugins/` directory

3. **Start Server**:
   - The plugin will auto-generate `config.toml` on first run
   - Configure settings in `plugins/OnistoneBuilder/config.toml`

4. **Assign Permissions**:
   - Use your permission plugin to grant `onistone.builder.*` permissions
   - See [Permissions](#-permissions) section for details

---

## 🚀 Quick Start

### For Players

1. **Open Builder Menu**:
   ```
   /builder
   ```

2. **Enable Wand Tool** (optional):
   ```
   /builder wand
   ```
   - Left-click block = Set Position 1
   - Right-click block = Set Position 2

3. **Set Selection**:
   ```
   /builder pos1
   /builder pos2
   ```

4. **Copy/Paste**:
   - Open menu → Clipboard → Copy Selection
   - Move to new location
   - Open menu → Clipboard → Paste

5. **Save Blueprint**:
   - Open menu → Blueprints → Save Blueprint
   - Enter name and save

### For Operators

1. **Create Builder Zone**:
   ```
   /builder zone here <radius> [hours]
   ```
   Example: `/builder zone here 32 12` (32 block radius, 12 hour duration)

2. **Grant Builder Permissions**:
   ```
   /builder promote <player>
   ```

3. **Configure Settings**:
   - Edit `plugins/OnistoneBuilder/config.toml`
   - Adjust limits, zones, and features

---

## 📋 Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/builder` | Open main builder menu | `onistone.builder.menu` |
| `/builder wand` | Toggle wand tool | `onistone.builder.select` |
| `/builder pos1` | Set position 1 at current location | `onistone.builder.select` |
| `/builder pos2` | Set position 2 at current location | `onistone.builder.select` |
| `/builder undo` | Undo last paste/cut operation | `onistone.builder.paste` |
| `/builder zone here <radius> [hours]` | Create temporary builder zone | `onistone.builder.zone` |
| `/builder promote <player>` | Grant builder permissions (admin) | `onistone.builder.admin` |

---

## 🔐 Permissions

### Permission Nodes

| Permission | Description | Default |
|------------|-------------|---------|
| `onistone.builder.menu` | Access builder menu | `true` |
| `onistone.builder.select` | Use selection tools | `true` |
| `onistone.builder.copy` | Copy selections | `true` |
| `onistone.builder.cut` | Cut selections | `true` |
| `onistone.builder.paste` | Paste from clipboard | `true` |
| `onistone.builder.blueprint.save` | Save blueprints | `true` |
| `onistone.builder.blueprint.shared` | Access shared blueprints | `true` |
| `onistone.builder.blueprint.publish` | Publish blueprints | `op` |
| `onistone.builder.zone` | Create builder zones | `op` |
| `onistone.builder.bypass.zone` | Build outside zones | `op` |
| `onistone.builder.inventory.copy` | Copy block entities | `op` |
| `onistone.builder.entity.copy` | Copy entities | `op` |
| `onistone.builder.admin` | Admin tools | `op` |

### Recommended Permission Sets

**Basic Builder**:
```
onistone.builder.menu
onistone.builder.select
onistone.builder.copy
onistone.builder.paste
onistone.builder.blueprint.save
```

**Advanced Builder**:
```
onistone.builder.*
-onistone.builder.admin
-onistone.builder.bypass.zone
```

**Zone Manager**:
```
onistone.builder.*
onistone.builder.zone
```

---

## ⚙️ Configuration

Key configuration options in `config.toml`:

### Limits
- `maxSelectionVolume`: Maximum selection size (default: 250,000 blocks)
- `maxPasteVolume`: Maximum paste size (default: 100,000 blocks)
- `undoDepth`: Undo history depth (default: 5)
- `clipboardLimit`: Clipboard entries per player (default: 10)

### Zones
- `requireZone`: Require builder zones for edits (default: true)
- `defaultRadius`: Default zone radius (default: 32)
- `defaultDurationHours`: Default zone duration (default: 12 hours)

### Performance
- `batchSize`: Blocks per tick during paste (default: 4096)
- `ghostPreviewTimeoutSeconds`: Preview timeout (default: 120)

See `config.toml` for full configuration options.

---

## 📖 Usage Examples

### Example 1: Copy a House
```
1. Stand at one corner: /builder pos1
2. Stand at opposite corner: /builder pos2
3. /builder → Clipboard → Copy Selection
4. Move to new location
5. /builder → Clipboard → Paste
```

### Example 2: Save a Build as Blueprint
```
1. Select your build (pos1/pos2)
2. /builder → Clipboard → Copy Selection
3. /builder → Blueprints → Save Blueprint
4. Enter name: "my_awesome_house"
```

### Example 3: Create a Builder Zone
```
/builder zone here 48 24
```
Creates a 48-block radius zone lasting 24 hours.

---

## 🛠️ Technical Details

### Architecture
- **Pure Python**: No JavaScript/TypeScript, no behavior packs
- **Server-Side Only**: No client mods required
- **Endstone API**: Uses Endstone v0.5.0+ plugin framework
- **Server-UI**: Python library for interactive forms

### Data Storage
- **Blueprints**: JSON with palette mapping + RLE compression + zlib
- **Clipboard**: In-memory ring buffer per player
- **Undo**: Diff-based storage (only changed blocks)
- **Zones**: In-memory with periodic cleanup

### Performance
- **Async Paste**: Batched block placement to prevent lag
- **Compression**: RLE + zlib reduces blueprint file sizes by ~70%
- **Efficient Storage**: Palette-based block storage

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **Endstone Team**: For the amazing Bedrock server framework
- **server-ui**: For the Python UI library
- **WorldEdit**: Inspiration for selection and clipboard systems

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/OnistoneBuilderLite/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/OnistoneBuilderLite/discussions)

---

**Made with ❤️ for the Minecraft Bedrock community**

