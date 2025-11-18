"""Clipboard management for OnistoneBuilderLite."""

from collections import deque
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from dataclasses import dataclass

from .storage import BlockData
from .selection import Position

if TYPE_CHECKING:
    from endstone.level import Dimension


@dataclass
class ClipboardEntry:
    """Represents a clipboard entry."""
    blocks: List[BlockData]
    dimensions: tuple[int, int, int]
    origin: Position
    include_air: bool = True
    block_entities: Dict[tuple[int, int, int], Dict[str, Any]] = None
    entities: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize optional fields."""
        if self.block_entities is None:
            self.block_entities = {}
        if self.entities is None:
            self.entities = []
    
    def get_block_count(self) -> int:
        """Get non-air block count.
        
        Returns:
            Number of non-air blocks
        """
        return sum(1 for b in self.blocks if b.block_type != "minecraft:air")
    
    def get_index(self, x: int, y: int, z: int) -> int:
        """Get block index from relative coordinates.
        
        Args:
            x: Relative X coordinate
            y: Relative Y coordinate
            z: Relative Z coordinate
            
        Returns:
            Block index in blocks list
        """
        width, height, length = self.dimensions
        return x + z * width + y * width * length


class ClipboardManager:
    """Manages player clipboards with ring buffer."""
    
    def __init__(self, max_size: int = 10):
        """Initialize clipboard manager.
        
        Args:
            max_size: Maximum clipboard entries per player
        """
        self.max_size = max_size
        self.clipboards: Dict[str, deque[ClipboardEntry]] = {}
    
    def get_clipboard(self, player_uuid: str) -> deque[ClipboardEntry]:
        """Get or create clipboard for player.
        
        Args:
            player_uuid: Player UUID
            
        Returns:
            Player's clipboard deque
        """
        if player_uuid not in self.clipboards:
            self.clipboards[player_uuid] = deque(maxlen=self.max_size)
        return self.clipboards[player_uuid]
    
    def add_entry(self, player_uuid: str, entry: ClipboardEntry) -> None:
        """Add entry to player's clipboard.
        
        Args:
            player_uuid: Player UUID
            entry: Clipboard entry to add
        """
        clipboard = self.get_clipboard(player_uuid)
        clipboard.append(entry)
    
    def get_latest(self, player_uuid: str) -> Optional[ClipboardEntry]:
        """Get latest clipboard entry.
        
        Args:
            player_uuid: Player UUID
            
        Returns:
            Latest clipboard entry or None
        """
        clipboard = self.get_clipboard(player_uuid)
        return clipboard[-1] if clipboard else None
    
    def get_entry(self, player_uuid: str, index: int) -> Optional[ClipboardEntry]:
        """Get clipboard entry by index.
        
        Args:
            player_uuid: Player UUID
            index: Entry index (0 = oldest, -1 = newest)
            
        Returns:
            Clipboard entry or None
        """
        clipboard = self.get_clipboard(player_uuid)
        try:
            return clipboard[index]
        except IndexError:
            return None
    
    def get_count(self, player_uuid: str) -> int:
        """Get clipboard entry count.
        
        Args:
            player_uuid: Player UUID
            
        Returns:
            Number of clipboard entries
        """
        return len(self.get_clipboard(player_uuid))
    
    def clear(self, player_uuid: str) -> None:
        """Clear player's clipboard.
        
        Args:
            player_uuid: Player UUID
        """
        if player_uuid in self.clipboards:
            self.clipboards[player_uuid].clear()
    
    def copy_region(
        self,
        dimension: "Dimension",
        min_pos: Position,
        max_pos: Position,
        origin: Position,
        include_air: bool = True,
        include_block_entities: bool = False,
        include_entities: bool = False
    ) -> ClipboardEntry:
        """Copy region to clipboard entry.
        
        Args:
            dimension: Dimension to copy from
            min_pos: Minimum position
            max_pos: Maximum position
            origin: Origin position (usually player location)
            include_air: Whether to include air blocks
            include_block_entities: Whether to include block entities
            include_entities: Whether to include entities
            
        Returns:
            Clipboard entry with copied data
        """
        width = max_pos.x - min_pos.x + 1
        height = max_pos.y - min_pos.y + 1
        length = max_pos.z - min_pos.z + 1
        
        blocks: List[BlockData] = []
        block_entities: Dict[tuple[int, int, int], Dict[str, Any]] = {}
        
        # Copy blocks
        for y in range(min_pos.y, max_pos.y + 1):
            for z in range(min_pos.z, max_pos.z + 1):
                for x in range(min_pos.x, max_pos.x + 1):
                    block = dimension.get_block_at(x, y, z)
                    block_type = block.type
                    block_data = block.data if hasattr(block, "data") else 0
                    
                    blocks.append(BlockData(block_type, block_data))
        
        # TODO: Copy block entities and entities if permissions allow
        # This would require additional Endstone API support
        
        return ClipboardEntry(
            blocks=blocks,
            dimensions=(width, height, length),
            origin=origin,
            include_air=include_air,
            block_entities=block_entities,
            entities=[]
        )

