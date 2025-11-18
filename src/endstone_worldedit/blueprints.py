"""Blueprint management for WorldEdit."""

import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


class Blueprint:
    """Represents a saved blueprint."""

    def __init__(self, name: str, clipboard_data: Dict[str, Any], author: str = "Unknown"):
        """Initialize blueprint.

        Args:
            name: Blueprint name
            clipboard_data: Clipboard data from WorldEdit
            author: Blueprint author
        """
        self.name = name
        self.clipboard_data = clipboard_data
        self.author = author
        self.created = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "author": self.author,
            "created": self.created,
            "clipboard": self.clipboard_data
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Blueprint":
        """Create blueprint from dictionary.

        Args:
            data: Dictionary data

        Returns:
            Blueprint instance
        """
        bp = Blueprint(
            name=data.get("name", "Unnamed"),
            clipboard_data=data.get("clipboard", {}),
            author=data.get("author", "Unknown")
        )
        bp.created = data.get("created", datetime.now().isoformat())
        return bp


class BlueprintManager:
    """Manages blueprint storage and loading."""
    
    def __init__(self, blueprint_folder: str, shared_folder: str):
        """Initialize blueprint manager.
        
        Args:
            blueprint_folder: Base blueprint folder path
            shared_folder: Shared blueprint folder path
        """
        self.blueprint_folder = Path(blueprint_folder)
        self.shared_folder = Path(shared_folder)
        
        # Create directories
        self.blueprint_folder.mkdir(parents=True, exist_ok=True)
        self.shared_folder.mkdir(parents=True, exist_ok=True)
    
    def get_personal_folder(self, player_uuid: str) -> Path:
        """Get personal blueprint folder for player.
        
        Args:
            player_uuid: Player UUID
            
        Returns:
            Path to personal folder
        """
        folder = self.blueprint_folder / "personal" / player_uuid
        folder.mkdir(parents=True, exist_ok=True)
        return folder
    
    def save_blueprint(
        self,
        player_uuid: str,
        name: str,
        clipboard_data: Dict[str, Any],
        author: str = "",
        shared: bool = False
    ) -> bool:
        """Save blueprint to file.

        Args:
            player_uuid: Player UUID
            name: Blueprint name
            clipboard_data: Clipboard data to save (from WorldEdit)
            author: Blueprint author
            shared: Whether to save to shared folder

        Returns:
            True if saved successfully
        """
        try:
            blueprint = Blueprint(name, clipboard_data, author)

            # Determine save location
            if shared:
                folder = self.shared_folder
            else:
                folder = self.get_personal_folder(player_uuid)

            # Save to file
            file_path = folder / f"{name}.json"
            with open(file_path, "w") as f:
                json.dump(blueprint.to_dict(), f, indent=2)

            return True
        except Exception as e:
            print(f"[WorldEdit] Error saving blueprint: {e}")
            return False
    
    def load_blueprint(
        self,
        player_uuid: str,
        name: str,
        from_shared: bool = False
    ) -> Optional[Blueprint]:
        """Load blueprint from file.

        Args:
            player_uuid: Player UUID
            name: Blueprint name
            from_shared: Whether to load from shared folder

        Returns:
            Blueprint or None if not found
        """
        try:
            # Determine load location
            if from_shared:
                folder = self.shared_folder
            else:
                folder = self.get_personal_folder(player_uuid)

            file_path = folder / f"{name}.json"

            if not file_path.exists():
                return None

            with open(file_path, "r") as f:
                data = json.load(f)

            return Blueprint.from_dict(data)
        except Exception as e:
            print(f"[WorldEdit] Error loading blueprint: {e}")
            return None

    def list_blueprints(self, player_uuid: str, include_shared: bool = True) -> List[str]:
        """List available blueprints.

        Args:
            player_uuid: Player UUID
            include_shared: Whether to include shared blueprints

        Returns:
            List of blueprint names
        """
        blueprints = []

        # Personal blueprints
        personal_folder = self.get_personal_folder(player_uuid)
        for file in personal_folder.glob("*.json"):
            blueprints.append(file.stem)

        # Shared blueprints
        if include_shared:
            for file in self.shared_folder.glob("*.json"):
                blueprints.append(f"[Shared] {file.stem}")

        return sorted(blueprints)

    def delete_blueprint(self, player_uuid: str, name: str, from_shared: bool = False) -> bool:
        """Delete blueprint file.

        Args:
            player_uuid: Player UUID
            name: Blueprint name
            from_shared: Whether to delete from shared folder

        Returns:
            True if deleted successfully
        """
        try:
            if from_shared:
                folder = self.shared_folder
            else:
                folder = self.get_personal_folder(player_uuid)

            file_path = folder / f"{name}.json"

            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"[WorldEdit] Error deleting blueprint: {e}")
            return False

