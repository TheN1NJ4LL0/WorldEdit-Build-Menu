"""Blueprint management for OnistoneBuilderLite."""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from .storage import BlockData, RLECompressor, BlueprintMetadata
from .clipboard import ClipboardEntry


class Blueprint:
    """Represents a saved blueprint."""
    
    def __init__(self, metadata: BlueprintMetadata, clipboard: ClipboardEntry):
        """Initialize blueprint.
        
        Args:
            metadata: Blueprint metadata
            clipboard: Clipboard data
        """
        self.metadata = metadata
        self.clipboard = clipboard
        
        # Update metadata from clipboard
        self.metadata.dimensions = clipboard.dimensions
        self.metadata.block_count = clipboard.get_block_count()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization.
        
        Returns:
            Dictionary representation
        """
        return {
            "metadata": self.metadata.to_dict(),
            "dimensions": self.clipboard.dimensions,
            "origin": self.clipboard.origin.to_tuple(),
            "includeAir": self.clipboard.include_air,
            "blocks": RLECompressor.compress(self.clipboard.blocks).hex(),
            "blockEntities": {
                f"{k[0]},{k[1]},{k[2]}": v 
                for k, v in self.clipboard.block_entities.items()
            },
            "entities": self.clipboard.entities,
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Blueprint":
        """Create blueprint from dictionary.
        
        Args:
            data: Dictionary data
            
        Returns:
            Blueprint instance
        """
        from .selection import Position
        
        metadata = BlueprintMetadata.from_dict(data["metadata"])
        
        blocks = RLECompressor.decompress(bytes.fromhex(data["blocks"]))
        
        block_entities = {
            tuple(map(int, k.split(","))): v
            for k, v in data.get("blockEntities", {}).items()
        }
        
        origin_tuple = data.get("origin", (0, 0, 0))
        origin = Position(*origin_tuple)
        
        clipboard = ClipboardEntry(
            blocks=blocks,
            dimensions=tuple(data["dimensions"]),
            origin=origin,
            include_air=data.get("includeAir", True),
            block_entities=block_entities,
            entities=data.get("entities", [])
        )
        
        return Blueprint(metadata, clipboard)


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
        clipboard: ClipboardEntry,
        description: str = "",
        author: str = "",
        shared: bool = False
    ) -> bool:
        """Save blueprint to file.
        
        Args:
            player_uuid: Player UUID
            name: Blueprint name
            clipboard: Clipboard data to save
            description: Blueprint description
            author: Blueprint author
            shared: Whether to save to shared folder
            
        Returns:
            True if saved successfully
        """
        try:
            metadata = BlueprintMetadata(name, description, author)
            blueprint = Blueprint(metadata, clipboard)
            
            # Determine save location
            if shared:
                folder = self.shared_folder
            else:
                folder = self.get_personal_folder(player_uuid)
            
            # Save to file
            file_path = folder / f"{name}.bp"
            with open(file_path, "w") as f:
                json.dump(blueprint.to_dict(), f, indent=2)
            
            return True
        except Exception as e:
            print(f"[OnistoneBuilder] Error saving blueprint: {e}")
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
            
            file_path = folder / f"{name}.bp"
            
            if not file_path.exists():
                return None
            
            with open(file_path, "r") as f:
                data = json.load(f)
            
            return Blueprint.from_dict(data)
        except Exception as e:
            print(f"[OnistoneBuilder] Error loading blueprint: {e}")
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
        for file in personal_folder.glob("*.bp"):
            blueprints.append(file.stem)
        
        # Shared blueprints
        if include_shared:
            for file in self.shared_folder.glob("*.bp"):
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
            
            file_path = folder / f"{name}.bp"
            
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"[OnistoneBuilder] Error deleting blueprint: {e}")
            return False

