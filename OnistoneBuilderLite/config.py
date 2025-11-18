"""Configuration management for OnistoneBuilderLite."""

import os
from pathlib import Path
from typing import Any, Dict

try:
    import tomli as tomllib
except ImportError:
    import tomllib


class Config:
    """Manages plugin configuration from config.toml."""
    
    DEFAULT_CONFIG = {
        "limits": {
            "maxSelectionVolume": 250000,
            "maxPasteVolume": 100000,
            "undoDepth": 5,
            "clipboardLimit": 10,
            "confirmThreshold": 5000,
        },
        "zones": {
            "requireZone": True,
            "defaultRadius": 32,
            "defaultDurationHours": 12,
        },
        "permissions": {
            "allowInventories": False,
            "allowEntities": False,
        },
        "paths": {
            "blueprintFolder": "plugins/OnistoneBuilder/blueprints",
            "sharedFolder": "plugins/OnistoneBuilder/blueprints/shared",
        },
        "performance": {
            "batchSize": 4096,
            "ghostPreviewTimeoutSeconds": 120,
        },
    }
    
    def __init__(self, config_path: str):
        """Initialize configuration.
        
        Args:
            config_path: Path to config.toml file
        """
        self.config_path = Path(config_path)
        self.data: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from file or use defaults."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "rb") as f:
                    self.data = tomllib.load(f)
                # Merge with defaults for missing keys
                self._merge_defaults()
            except Exception as e:
                print(f"[OnistoneBuilder] Error loading config: {e}, using defaults")
                self.data = self.DEFAULT_CONFIG.copy()
        else:
            print("[OnistoneBuilder] Config not found, using defaults")
            self.data = self.DEFAULT_CONFIG.copy()
            self._create_default_config()
    
    def _merge_defaults(self) -> None:
        """Merge loaded config with defaults for missing keys."""
        for section, values in self.DEFAULT_CONFIG.items():
            if section not in self.data:
                self.data[section] = values.copy()
            else:
                for key, default_value in values.items():
                    if key not in self.data[section]:
                        self.data[section][key] = default_value
    
    def _create_default_config(self) -> None:
        """Create default config.toml file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w") as f:
                f.write(self._generate_toml())
            print(f"[OnistoneBuilder] Created default config at {self.config_path}")
        except Exception as e:
            print(f"[OnistoneBuilder] Failed to create config file: {e}")
    
    def _generate_toml(self) -> str:
        """Generate TOML string from default config."""
        lines = []
        for section, values in self.DEFAULT_CONFIG.items():
            lines.append(f"[{section}]")
            for key, value in values.items():
                if isinstance(value, str):
                    lines.append(f'{key} = "{value}"')
                elif isinstance(value, bool):
                    lines.append(f'{key} = {str(value).lower()}')
                else:
                    lines.append(f'{key} = {value}')
            lines.append("")
        return "\n".join(lines)
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found
            
        Returns:
            Configuration value or default
        """
        return self.data.get(section, {}).get(key, default)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section.
        
        Args:
            section: Configuration section name
            
        Returns:
            Dictionary of section values
        """
        return self.data.get(section, {})
    
    def set(self, section: str, key: str, value: Any) -> None:
        """Set configuration value at runtime.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value

