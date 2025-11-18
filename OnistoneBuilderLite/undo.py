"""Undo system for OnistoneBuilderLite."""

from collections import deque
from typing import List, Dict, Tuple, Optional, TYPE_CHECKING
from dataclasses import dataclass

from .storage import BlockData
from .selection import Position

if TYPE_CHECKING:
    from endstone.level import Dimension


@dataclass
class BlockChange:
    """Represents a single block change."""
    position: Position
    old_block: BlockData
    new_block: BlockData
    dimension: str


class UndoEntry:
    """Represents an undo entry with multiple block changes."""
    
    def __init__(self, description: str = ""):
        """Initialize undo entry.
        
        Args:
            description: Description of the action
        """
        self.description = description
        self.changes: List[BlockChange] = []
    
    def add_change(self, change: BlockChange) -> None:
        """Add a block change.
        
        Args:
            change: Block change to add
        """
        self.changes.append(change)
    
    def get_block_count(self) -> int:
        """Get number of blocks changed.
        
        Returns:
            Number of block changes
        """
        return len(self.changes)


class UndoManager:
    """Manages per-player undo history."""
    
    def __init__(self, max_depth: int = 5):
        """Initialize undo manager.
        
        Args:
            max_depth: Maximum undo depth per player
        """
        self.max_depth = max_depth
        self.undo_stacks: Dict[str, deque[UndoEntry]] = {}
    
    def get_undo_stack(self, player_uuid: str) -> deque[UndoEntry]:
        """Get or create undo stack for player.
        
        Args:
            player_uuid: Player UUID
            
        Returns:
            Player's undo stack
        """
        if player_uuid not in self.undo_stacks:
            self.undo_stacks[player_uuid] = deque(maxlen=self.max_depth)
        return self.undo_stacks[player_uuid]
    
    def add_entry(self, player_uuid: str, entry: UndoEntry) -> None:
        """Add undo entry for player.
        
        Args:
            player_uuid: Player UUID
            entry: Undo entry to add
        """
        stack = self.get_undo_stack(player_uuid)
        stack.append(entry)
    
    def can_undo(self, player_uuid: str) -> bool:
        """Check if player can undo.
        
        Args:
            player_uuid: Player UUID
            
        Returns:
            True if undo is available
        """
        stack = self.get_undo_stack(player_uuid)
        return len(stack) > 0
    
    def get_undo_count(self, player_uuid: str) -> int:
        """Get undo entry count.
        
        Args:
            player_uuid: Player UUID
            
        Returns:
            Number of undo entries
        """
        return len(self.get_undo_stack(player_uuid))
    
    def undo(self, player_uuid: str, dimension: "Dimension") -> Optional[UndoEntry]:
        """Perform undo operation.
        
        Args:
            player_uuid: Player UUID
            dimension: Dimension to undo in
            
        Returns:
            Undone entry or None if no undo available
        """
        stack = self.get_undo_stack(player_uuid)
        if not stack:
            return None
        
        entry = stack.pop()
        
        # Restore blocks in reverse order
        for change in reversed(entry.changes):
            if change.dimension == dimension.name:
                block = dimension.get_block_at(
                    change.position.x,
                    change.position.y,
                    change.position.z
                )
                block.set_type(change.old_block.block_type)
                if hasattr(block, "set_data"):
                    block.set_data(change.old_block.data)
        
        return entry
    
    def clear(self, player_uuid: str) -> None:
        """Clear player's undo history.
        
        Args:
            player_uuid: Player UUID
        """
        if player_uuid in self.undo_stacks:
            self.undo_stacks[player_uuid].clear()
    
    def record_paste(
        self,
        player_uuid: str,
        dimension: "Dimension",
        positions: List[Position],
        description: str = "Paste"
    ) -> UndoEntry:
        """Record a paste operation for undo.
        
        Args:
            player_uuid: Player UUID
            dimension: Dimension where paste occurred
            positions: List of positions that were modified
            description: Description of the operation
            
        Returns:
            Created undo entry
        """
        entry = UndoEntry(description)
        
        # Record current state of all positions
        for pos in positions:
            block = dimension.get_block_at(pos.x, pos.y, pos.z)
            old_block = BlockData(
                block.type,
                block.data if hasattr(block, "data") else 0
            )
            
            # We don't know the new block yet, will be set during paste
            # For now, just record the old state
            change = BlockChange(
                position=pos,
                old_block=old_block,
                new_block=old_block,  # Will be updated during paste
                dimension=dimension.name
            )
            entry.add_change(change)
        
        self.add_entry(player_uuid, entry)
        return entry
    
    def get_latest_description(self, player_uuid: str) -> Optional[str]:
        """Get description of latest undo entry.
        
        Args:
            player_uuid: Player UUID
            
        Returns:
            Description or None
        """
        stack = self.get_undo_stack(player_uuid)
        if stack:
            return stack[-1].description
        return None

