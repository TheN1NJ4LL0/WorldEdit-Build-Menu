"""Selection management for OnistoneBuilderLite."""

from typing import Optional, Tuple, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from endstone.level import Dimension, Location


@dataclass
class Position:
    """3D position."""
    x: int
    y: int
    z: int
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to tuple."""
        return (self.x, self.y, self.z)
    
    @staticmethod
    def from_location(loc: "Location") -> "Position":
        """Create from Endstone Location."""
        return Position(int(loc.x), int(loc.y), int(loc.z))


class Selection:
    """Represents a cuboid selection."""
    
    def __init__(self):
        """Initialize empty selection."""
        self.pos1: Optional[Position] = None
        self.pos2: Optional[Position] = None
        self.dimension: Optional[str] = None
    
    def set_pos1(self, pos: Position, dimension: str) -> None:
        """Set position 1.
        
        Args:
            pos: Position to set
            dimension: Dimension name
        """
        self.pos1 = pos
        if self.dimension is None:
            self.dimension = dimension
    
    def set_pos2(self, pos: Position, dimension: str) -> None:
        """Set position 2.
        
        Args:
            pos: Position to set
            dimension: Dimension name
        """
        self.pos2 = pos
        if self.dimension is None:
            self.dimension = dimension
    
    def is_complete(self) -> bool:
        """Check if selection is complete.
        
        Returns:
            True if both positions are set
        """
        return self.pos1 is not None and self.pos2 is not None
    
    def get_bounds(self) -> Optional[Tuple[Position, Position]]:
        """Get selection bounds (min, max).
        
        Returns:
            Tuple of (min_pos, max_pos) or None if incomplete
        """
        if not self.is_complete():
            return None
        
        min_x = min(self.pos1.x, self.pos2.x)
        min_y = min(self.pos1.y, self.pos2.y)
        min_z = min(self.pos1.z, self.pos2.z)
        
        max_x = max(self.pos1.x, self.pos2.x)
        max_y = max(self.pos1.y, self.pos2.y)
        max_z = max(self.pos1.z, self.pos2.z)
        
        return (Position(min_x, min_y, min_z), Position(max_x, max_y, max_z))
    
    def get_dimensions(self) -> Optional[Tuple[int, int, int]]:
        """Get selection dimensions (width, height, length).
        
        Returns:
            Tuple of (width, height, length) or None if incomplete
        """
        bounds = self.get_bounds()
        if not bounds:
            return None
        
        min_pos, max_pos = bounds
        width = max_pos.x - min_pos.x + 1
        height = max_pos.y - min_pos.y + 1
        length = max_pos.z - min_pos.z + 1
        
        return (width, height, length)
    
    def get_volume(self) -> int:
        """Get selection volume in blocks.
        
        Returns:
            Volume in blocks, or 0 if incomplete
        """
        dims = self.get_dimensions()
        if not dims:
            return 0
        
        width, height, length = dims
        return width * height * length
    
    def contains(self, pos: Position) -> bool:
        """Check if position is within selection.
        
        Args:
            pos: Position to check
            
        Returns:
            True if position is within selection
        """
        bounds = self.get_bounds()
        if not bounds:
            return False
        
        min_pos, max_pos = bounds
        return (min_pos.x <= pos.x <= max_pos.x and
                min_pos.y <= pos.y <= max_pos.y and
                min_pos.z <= pos.z <= max_pos.z)
    
    def clear(self) -> None:
        """Clear selection."""
        self.pos1 = None
        self.pos2 = None
        self.dimension = None
    
    def __str__(self) -> str:
        """String representation."""
        if not self.is_complete():
            return "Incomplete selection"
        
        dims = self.get_dimensions()
        volume = self.get_volume()
        return f"{dims[0]}×{dims[1]}×{dims[2]} ({volume:,} blocks)"


class SelectionManager:
    """Manages player selections."""
    
    def __init__(self):
        """Initialize selection manager."""
        self.selections: dict[str, Selection] = {}
    
    def get_selection(self, player_uuid: str) -> Selection:
        """Get or create selection for player.
        
        Args:
            player_uuid: Player UUID
            
        Returns:
            Player's selection
        """
        if player_uuid not in self.selections:
            self.selections[player_uuid] = Selection()
        return self.selections[player_uuid]
    
    def clear_selection(self, player_uuid: str) -> None:
        """Clear player's selection.
        
        Args:
            player_uuid: Player UUID
        """
        if player_uuid in self.selections:
            self.selections[player_uuid].clear()

