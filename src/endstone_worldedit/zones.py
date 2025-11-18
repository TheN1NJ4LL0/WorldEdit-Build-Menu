"""Builder zone management for WorldEdit."""

from datetime import datetime, timedelta
from typing import Optional, List, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class BuilderZone:
    """Represents a temporary builder zone."""
    name: str
    owner: str
    min_pos: Tuple[int, int, int]  # (x, y, z)
    max_pos: Tuple[int, int, int]  # (x, y, z)
    dimension: str
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    shared_with: Set[str] = field(default_factory=set)
    
    def is_expired(self) -> bool:
        """Check if zone has expired.
        
        Returns:
            True if zone is expired
        """
        if self.expires_at is None:
            return False
        return datetime.now() >= self.expires_at
    
    def contains(self, pos: Tuple[int, int, int], dimension: str) -> bool:
        """Check if position is within zone.

        Args:
            pos: Position tuple (x, y, z) to check
            dimension: Dimension name

        Returns:
            True if position is within zone
        """
        if dimension != self.dimension:
            return False

        x, y, z = pos
        return (self.min_pos[0] <= x <= self.max_pos[0] and
                self.min_pos[1] <= y <= self.max_pos[1] and
                self.min_pos[2] <= z <= self.max_pos[2])
    
    def has_access(self, player_name: str) -> bool:
        """Check if player has access to zone.
        
        Args:
            player_name: Player name to check
            
        Returns:
            True if player has access
        """
        return player_name == self.owner or player_name in self.shared_with
    
    def add_builder(self, player_name: str) -> None:
        """Add builder to zone.
        
        Args:
            player_name: Player name to add
        """
        self.shared_with.add(player_name)
    
    def remove_builder(self, player_name: str) -> None:
        """Remove builder from zone.
        
        Args:
            player_name: Player name to remove
        """
        self.shared_with.discard(player_name)
    
    def get_volume(self) -> int:
        """Get zone volume.

        Returns:
            Volume in blocks
        """
        width = self.max_pos[0] - self.min_pos[0] + 1
        height = self.max_pos[1] - self.min_pos[1] + 1
        length = self.max_pos[2] - self.min_pos[2] + 1
        return width * height * length

    def get_center(self) -> Tuple[int, int, int]:
        """Get zone center position.

        Returns:
            Center position tuple (x, y, z)
        """
        x = (self.min_pos[0] + self.max_pos[0]) // 2
        y = (self.min_pos[1] + self.max_pos[1]) // 2
        z = (self.min_pos[2] + self.max_pos[2]) // 2
        return (x, y, z)


class ZoneManager:
    """Manages builder zones."""
    
    def __init__(self):
        """Initialize zone manager."""
        self.zones: List[BuilderZone] = []
    
    def create_zone(
        self,
        name: str,
        owner: str,
        min_pos: Tuple[int, int, int],
        max_pos: Tuple[int, int, int],
        dimension: str,
        duration_hours: Optional[float] = None
    ) -> BuilderZone:
        """Create a new builder zone.

        Args:
            name: Zone name
            owner: Zone owner
            min_pos: Minimum position tuple (x, y, z)
            max_pos: Maximum position tuple (x, y, z)
            dimension: Dimension name
            duration_hours: Zone duration in hours (None = permanent)

        Returns:
            Created zone
        """
        expires_at = None
        if duration_hours is not None:
            expires_at = datetime.now() + timedelta(hours=duration_hours)
        
        zone = BuilderZone(
            name=name,
            owner=owner,
            min_pos=min_pos,
            max_pos=max_pos,
            dimension=dimension,
            expires_at=expires_at
        )
        
        self.zones.append(zone)
        return zone
    
    def create_zone_at_location(
        self,
        name: str,
        owner: str,
        center: Tuple[int, int, int],
        dimension: str,
        radius: int,
        duration_hours: Optional[float] = None
    ) -> BuilderZone:
        """Create zone centered at location.

        Args:
            name: Zone name
            owner: Zone owner
            center: Center position tuple (x, y, z)
            dimension: Dimension name
            radius: Zone radius
            duration_hours: Zone duration in hours

        Returns:
            Created zone
        """
        min_pos = (center[0] - radius, center[1] - radius, center[2] - radius)
        max_pos = (center[0] + radius, center[1] + radius, center[2] + radius)

        return self.create_zone(name, owner, min_pos, max_pos, dimension, duration_hours)
    
    def get_zone(self, name: str) -> Optional[BuilderZone]:
        """Get zone by name.
        
        Args:
            name: Zone name
            
        Returns:
            Zone or None if not found
        """
        for zone in self.zones:
            if zone.name.lower() == name.lower():
                return zone
        return None
    
    def delete_zone(self, name: str) -> bool:
        """Delete zone by name.
        
        Args:
            name: Zone name
            
        Returns:
            True if zone was deleted
        """
        zone = self.get_zone(name)
        if zone:
            self.zones.remove(zone)
            return True
        return False
    
    def get_zones_at_location(self, pos: Tuple[int, int, int], dimension: str) -> List[BuilderZone]:
        """Get all zones containing position.

        Args:
            pos: Position tuple (x, y, z) to check
            dimension: Dimension name

        Returns:
            List of zones containing position
        """
        return [z for z in self.zones if z.contains(pos, dimension) and not z.is_expired()]

    def can_build_at(self, player_name: str, pos: Tuple[int, int, int], dimension: str, bypass: bool = False) -> bool:
        """Check if player can build at location.
        
        Args:
            player_name: Player name
            pos: Position to check
            dimension: Dimension name
            bypass: Whether player has bypass permission
            
        Returns:
            True if player can build
        """
        if bypass:
            return True
        
        zones = self.get_zones_at_location(pos, dimension)
        if not zones:
            return False  # No zone = can't build (if requireZone is True)
        
        return any(z.has_access(player_name) for z in zones)
    
    def purge_expired(self) -> int:
        """Remove expired zones.
        
        Returns:
            Number of zones removed
        """
        before_count = len(self.zones)
        self.zones = [z for z in self.zones if not z.is_expired()]
        return before_count - len(self.zones)
    
    def get_player_zones(self, player_name: str) -> List[BuilderZone]:
        """Get all zones player has access to.
        
        Args:
            player_name: Player name
            
        Returns:
            List of accessible zones
        """
        return [z for z in self.zones if z.has_access(player_name) and not z.is_expired()]

