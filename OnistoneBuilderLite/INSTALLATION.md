# OnistoneBuilderLite - Installation Guide

This guide will walk you through installing and configuring OnistoneBuilderLite on your Minecraft Bedrock server running Endstone.

---

## 📋 Prerequisites

Before installing OnistoneBuilderLite, ensure you have:

1. **Minecraft Bedrock Dedicated Server** (1.21.111+)
2. **Endstone** (v0.5.0 or higher) installed and running
3. **Python 3.9+** installed on your server
4. **pip** (Python package manager)

---

## 🔧 Installation Steps

### Step 1: Install Python Dependencies

Open a terminal/command prompt and run:

```bash
pip install endstone>=0.5.0 server-ui>=2.1.0b0
```

**Note**: If you're using a virtual environment (recommended), activate it first:

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 2: Install the Plugin

#### Option A: Manual Installation

1. Download the `OnistoneBuilderLite` folder
2. Copy it to your server's `plugins/` directory
3. The structure should look like:
   ```
   your-server/
   ├── plugins/
   │   └── OnistoneBuilderLite/
   │       ├── __init__.py
   │       ├── main.py
   │       ├── config.toml
   │       ├── plugin.yml
   │       └── ... (other files)
   └── ... (other server files)
   ```

#### Option B: Using pip (if packaged)

```bash
pip install onistone-builder-lite
```

### Step 3: Start Your Server

Start your Endstone server. The plugin will:
- Auto-load on startup
- Generate default configuration files
- Create necessary directories

You should see in the console:
```
[INFO] Loading OnistoneBuilderLite...
[INFO] OnistoneBuilderLite loaded successfully!
[INFO] Enabling OnistoneBuilderLite...
[INFO] OnistoneBuilderLite enabled!
```

### Step 4: Configure the Plugin

1. Stop your server
2. Navigate to `plugins/OnistoneBuilder/config.toml`
3. Edit settings as needed (see [Configuration](#-configuration) below)
4. Save and restart your server

---

## ⚙️ Configuration

### Basic Configuration

Edit `plugins/OnistoneBuilder/config.toml`:

```toml
[limits]
maxSelectionVolume = 250000  # Max selection size
maxPasteVolume = 100000      # Max paste size
undoDepth = 5                # Undo history depth
clipboardLimit = 10          # Clipboard entries per player

[zones]
requireZone = true           # Require zones for building
defaultRadius = 32           # Default zone radius
defaultDurationHours = 12    # Default zone duration

[performance]
batchSize = 4096            # Blocks per tick during paste
```

### Advanced Configuration

See `config.toml` for all available options including:
- Permission settings
- Path configurations
- Feature toggles
- Custom messages

---

## 🔐 Setting Up Permissions

### Using Endstone's Built-in Permissions

OnistoneBuilderLite uses the permission namespace `onistone.builder.*`

#### Grant All Builder Permissions:
```yaml
# In your permissions.yml or permission plugin
players:
  PlayerName:
    permissions:
      - onistone.builder.*
```

#### Grant Specific Permissions:
```yaml
players:
  PlayerName:
    permissions:
      - onistone.builder.menu
      - onistone.builder.select
      - onistone.builder.copy
      - onistone.builder.paste
```

### Permission Nodes Reference

| Permission | Description |
|------------|-------------|
| `onistone.builder.*` | All permissions |
| `onistone.builder.menu` | Access builder menu |
| `onistone.builder.select` | Use selection tools |
| `onistone.builder.copy` | Copy selections |
| `onistone.builder.cut` | Cut selections |
| `onistone.builder.paste` | Paste from clipboard |
| `onistone.builder.blueprint.save` | Save blueprints |
| `onistone.builder.zone` | Create zones (OP) |
| `onistone.builder.admin` | Admin tools (OP) |

---

## 🧪 Testing the Installation

### Test 1: Check Plugin Loaded

1. Join your server
2. Run `/plugins` or check console logs
3. Verify "OnistoneBuilderLite v1.0.0" is listed

### Test 2: Open Builder Menu

1. Run `/builder`
2. You should see the builder menu UI
3. If you get a permission error, check your permissions

### Test 3: Create a Selection

1. Run `/builder pos1`
2. Move to another location
3. Run `/builder pos2`
4. You should see selection confirmation messages

### Test 4: Copy and Paste

1. With a selection active, run `/builder`
2. Navigate to Clipboard → Copy Selection
3. Move to a new location
4. Navigate to Clipboard → Paste
5. Your selection should be pasted

---

## 🐛 Troubleshooting

### Plugin Not Loading

**Problem**: Plugin doesn't appear in `/plugins` list

**Solutions**:
- Check Python version: `python --version` (must be 3.9+)
- Verify dependencies: `pip list | grep endstone`
- Check server logs for errors
- Ensure `plugin.yml` exists in plugin folder

### Permission Errors

**Problem**: "You don't have permission" messages

**Solutions**:
- Grant `onistone.builder.*` permission
- Check if you're OP: `/op YourName`
- Verify permission plugin is working
- Check `plugin.yml` for default permissions

### UI Not Showing

**Problem**: `/builder` command works but no UI appears

**Solutions**:
- Verify `server-ui` is installed: `pip show server-ui`
- Check server-ui version: Must be 2.1.0-beta or higher
- Restart server after installing dependencies
- Check for conflicting plugins

### Paste Not Working

**Problem**: Paste command runs but blocks don't place

**Solutions**:
- Check if you're in a builder zone (if `requireZone = true`)
- Verify paste volume is within limits
- Check dimension matches (can't paste across dimensions)
- Ensure you have blocks in clipboard

### Zone Issues

**Problem**: Can't create zones or zones expire immediately

**Solutions**:
- Check `onistone.builder.zone` permission
- Verify `defaultDurationHours` in config
- Check server time/date is correct
- Ensure radius is within `maxRadius` limit

---

## 📁 File Structure

After installation, your plugin directory should look like:

```
plugins/
└── OnistoneBuilder/
    ├── config.toml                    # Main configuration
    ├── blueprints/                    # Blueprint storage
    │   ├── personal/                  # Personal blueprints
    │   │   └── <player-uuid>/
    │   │       └── *.bp
    │   ├── shared/                    # Shared blueprints
    │   │   └── *.bp
    │   └── published/                 # Published blueprints
    │       └── *.bp
    └── logs/                          # Plugin logs (if enabled)
```

---

## 🔄 Updating the Plugin

1. **Backup** your `config.toml` and `blueprints/` folder
2. Stop your server
3. Replace the `OnistoneBuilderLite/` folder with the new version
4. Restore your `config.toml` (merge new settings if needed)
5. Restore your `blueprints/` folder
6. Start your server

---

## 🆘 Getting Help

If you encounter issues:

1. **Check Logs**: Look in server console for error messages
2. **Read Documentation**: See README.md for usage details
3. **GitHub Issues**: Report bugs at [GitHub Issues](https://github.com/yourusername/OnistoneBuilderLite/issues)
4. **Community**: Ask in [GitHub Discussions](https://github.com/yourusername/OnistoneBuilderLite/discussions)

---

## ✅ Next Steps

After successful installation:

1. **Configure Limits**: Adjust `maxSelectionVolume` and `maxPasteVolume` for your server
2. **Set Up Zones**: Create builder zones for your players
3. **Grant Permissions**: Assign appropriate permissions to player groups
4. **Test Features**: Try all commands and menus
5. **Share Blueprints**: Set up shared blueprint folder for community builds

---

**Congratulations! OnistoneBuilderLite is now installed and ready to use! 🎉**

