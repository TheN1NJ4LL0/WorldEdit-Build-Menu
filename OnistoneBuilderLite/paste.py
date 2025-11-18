"""Paste operations for OnistoneBuilderLite."""

from typing import TYPE_CHECKING, List, Tuple, Optional
from enum import Enum
import math

from .clipboard import ClipboardEntry
from .selection import Position
from .storage import BlockData

if TYPE_CHECKING:
    from endstone.level import Dimension
    from endstone.player import Player


class Rotation(Enum):
    """Rotation angles."""
    NONE = 0
    ROTATE_90 = 90
    ROTATE_180 = 180
    ROTATE_270 = 270


class FlipAxis(Enum):
    """Flip axes."""
    NONE = 0
    X = 1
    Y = 2
    Z = 3


class PasteOptions:
    """Options for paste operation."""
    
    def __init__(self):
        """Initialize with default options."""
        self.rotation = Rotation.NONE
        self.flip_x = False
        self.flip_y = False
        self.flip_z = False
        self.offset_x = 0
        self.offset_y = 0
        self.offset_z = 0
        self.place_air = True
        self.ignore_liquids = False
        self.replace_only_same_type = False


class PasteOperation:
    """Handles paste operations with transforms."""
    
    def __init__(self, clipboard: ClipboardEntry, options: PasteOptions):
        """Initialize paste operation.
        
        Args:
            clipboard: Clipboard to paste
            options: Paste options
        """
        self.clipboard = clipboard
        self.options = options
    
    def _rotate_position(self, x: int, y: int, z: int, width: int, length: int) -> Tuple[int, int, int]:
        """Rotate position based on rotation setting.
        
        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
            width: Region width
            length: Region length
            
        Returns:
            Rotated (x, y, z) coordinates
        """
        if self.options.rotation == Rotation.ROTATE_90:
            return (length - 1 - z, y, x)
        elif self.options.rotation == Rotation.ROTATE_180:
            return (width - 1 - x, y, length - 1 - z)
        elif self.options.rotation == Rotation.ROTATE_270:
            return (z, y, width - 1 - x)
        return (x, y, z)
    
    def _flip_position(self, x: int, y: int, z: int, width: int, height: int, length: int) -> Tuple[int, int, int]:
        """Flip position based on flip settings.
        
        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
            width: Region width
            height: Region height
            length: Region length
            
        Returns:
            Flipped (x, y, z) coordinates
        """
        if self.options.flip_x:
            x = width - 1 - x
        if self.options.flip_y:
            y = height - 1 - y
        if self.options.flip_z:
            z = length - 1 - z
        return (x, y, z)
    
    def get_transformed_positions(self, target: Position) -> List[Tuple[Position, BlockData]]:
        """Get list of positions and blocks after transforms.
        
        Args:
            target: Target paste position
            
        Returns:
            List of (position, block) tuples
        """
        width, height, length = self.clipboard.dimensions
        result: List[Tuple[Position, BlockData]] = []
        
        for y in range(height):
            for z in range(length):
                for x in range(width):
                    # Get block from clipboard
                    idx = self.clipboard.get_index(x, y, z)
                    block = self.clipboard.blocks[idx]
                    
                    # Skip air if not placing air
                    if not self.options.place_air and block.block_type == "minecraft:air":
                        continue
                    
                    # Apply transforms
                    tx, ty, tz = self._rotate_position(x, y, z, width, length)
                    tx, ty, tz = self._flip_position(tx, ty, tz, width, height, length)
                    
                    # Apply offset
                    tx += self.options.offset_x
                    ty += self.options.offset_y
                    tz += self.options.offset_z
                    
                    # Calculate world position
                    world_pos = Position(
                        target.x + tx,
                        target.y + ty,
                        target.z + tz
                    )
                    
                    result.append((world_pos, block))
        
        return result
    
    def estimate_block_count(self) -> int:
        """Estimate number of blocks that will be placed.
        
        Returns:
            Estimated block count
        """
        if self.options.place_air:
            return len(self.clipboard.blocks)
        else:
            return self.clipboard.get_block_count()
    
    def get_affected_volume(self) -> int:
        """Get volume of affected region.
        
        Returns:
            Volume in blocks
        """
        width, height, length = self.clipboard.dimensions
        
        # Account for rotation
        if self.options.rotation in (Rotation.ROTATE_90, Rotation.ROTATE_270):
            width, length = length, width
        
        return width * height * length


class PasteExecutor:
    """Executes paste operations asynchronously."""
    
    def __init__(self, batch_size: int = 4096):
        """Initialize paste executor.
        
        Args:
            batch_size: Number of blocks per batch
        """
        self.batch_size = batch_size
    
    async def execute_paste(
        self,
        dimension: "Dimension",
        operation: PasteOperation,
        target: Position,
        player: Optional["Player"] = None
    ) -> int:
        """Execute paste operation.
        
        Args:
            dimension: Target dimension
            operation: Paste operation
            target: Target position
            player: Player executing paste (for messages)
            
        Returns:
            Number of blocks placed
        """
        positions = operation.get_transformed_positions(target)
        total_blocks = len(positions)
        placed_count = 0
        
        # Process in batches
        for i in range(0, total_blocks, self.batch_size):
            batch = positions[i:i + self.batch_size]
            
            for pos, block in batch:
                try:
                    world_block = dimension.get_block_at(pos.x, pos.y, pos.z)
                    
                    # Check replace conditions
                    if operation.options.ignore_liquids:
                        current_type = world_block.type
                        if "water" in current_type or "lava" in current_type:
                            continue
                    
                    if operation.options.replace_only_same_type:
                        if world_block.type != block.block_type:
                            continue
                    
                    # Place block
                    world_block.set_type(block.block_type)
                    if hasattr(world_block, "set_data"):
                        world_block.set_data(block.data)
                    
                    placed_count += 1
                except Exception as e:
                    print(f"[OnistoneBuilder] Error placing block at {pos}: {e}")
            
            # Send progress message
            if player and total_blocks > self.batch_size:
                progress = (i + len(batch)) / total_blocks * 100
                player.send_message(f"§7Pasting... {progress:.1f}% ({placed_count}/{total_blocks})§r")
        
        return placed_count

