"""
Build Area Management System
Manages designated build zones where builders can use WorldEdit commands
"""
import json
import os
from typing import Dict, List, Tuple, Optional


class BuildArea:
    """Represents a cuboid build area with permissions"""
    
    def __init__(self, name: str, world: str, pos1: Tuple[int, int, int], 
                 pos2: Tuple[int, int, int], builders: List[str] = None,
                 creative_mode: bool = True):
        self.name = name
        self.world = world
        self.pos1 = pos1
        self.pos2 = pos2
        self.builders = builders or []
        self.creative_mode = creative_mode
        
        # Calculate bounds
        self.min_x = min(pos1[0], pos2[0])
        self.max_x = max(pos1[0], pos2[0])
        self.min_y = min(pos1[1], pos2[1])
        self.max_y = max(pos1[1], pos2[1])
        self.min_z = min(pos1[2], pos2[2])
        self.max_z = max(pos1[2], pos2[2])
    
    def contains_point(self, x: float, y: float, z: float) -> bool:
        """Check if a point is within this build area"""
        return (self.min_x <= x <= self.max_x and
                self.min_y <= y <= self.max_y and
                self.min_z <= z <= self.max_z)
    
    def has_builder(self, player_name: str) -> bool:
        """Check if a player is authorized to build in this area"""
        return player_name in self.builders
    
    def add_builder(self, player_name: str):
        """Add a builder to this area"""
        if player_name not in self.builders:
            self.builders.append(player_name)
    
    def remove_builder(self, player_name: str):
        """Remove a builder from this area"""
        if player_name in self.builders:
            self.builders.remove(player_name)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "world": self.world,
            "pos1": self.pos1,
            "pos2": self.pos2,
            "builders": self.builders,
            "creative_mode": self.creative_mode
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'BuildArea':
        """Create BuildArea from dictionary"""
        return BuildArea(
            name=data["name"],
            world=data["world"],
            pos1=tuple(data["pos1"]),
            pos2=tuple(data["pos2"]),
            builders=data.get("builders", []),
            creative_mode=data.get("creative_mode", True)
        )
    
    def get_volume(self) -> int:
        """Calculate the volume of this build area"""
        return ((self.max_x - self.min_x + 1) * 
                (self.max_y - self.min_y + 1) * 
                (self.max_z - self.min_z + 1))
    
    def get_info(self) -> str:
        """Get formatted information about this build area"""
        builders_str = ", ".join(self.builders) if self.builders else "None"
        return (f"§6Build Area: §e{self.name}§r\n"
                f"§7World: §f{self.world}§r\n"
                f"§7Position 1: §f({self.pos1[0]}, {self.pos1[1]}, {self.pos1[2]})§r\n"
                f"§7Position 2: §f({self.pos2[0]}, {self.pos2[1]}, {self.pos2[2]})§r\n"
                f"§7Volume: §f{self.get_volume():,} blocks§r\n"
                f"§7Creative Mode: §f{'Enabled' if self.creative_mode else 'Disabled'}§r\n"
                f"§7Builders: §f{builders_str}§r")


class BuildAreaManager:
    """Manages all build areas"""
    
    def __init__(self, config_path: str = "plugins/WorldEdit/build_areas.json"):
        self.config_path = config_path
        self.areas: Dict[str, BuildArea] = {}
        self.load_areas()
    
    def load_areas(self):
        """Load build areas from JSON file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    self.areas = {
                        name: BuildArea.from_dict(area_data)
                        for name, area_data in data.items()
                    }
            except Exception as e:
                print(f"[WorldEdit] Error loading build areas: {e}")
                self.areas = {}
        else:
            self.areas = {}
            self.save_areas()
    
    def save_areas(self):
        """Save build areas to JSON file"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            data = {name: area.to_dict() for name, area in self.areas.items()}
            json.dump(data, f, indent=4)
    
    def create_area(self, name: str, world: str, pos1: Tuple[int, int, int], 
                    pos2: Tuple[int, int, int], creative_mode: bool = True) -> bool:
        """Create a new build area"""
        if name in self.areas:
            return False
        self.areas[name] = BuildArea(name, world, pos1, pos2, creative_mode=creative_mode)
        self.save_areas()
        return True
    
    def delete_area(self, name: str) -> bool:
        """Delete a build area"""
        if name in self.areas:
            del self.areas[name]
            self.save_areas()
            return True
        return False

    def get_area(self, name: str) -> Optional[BuildArea]:
        """Get a build area by name"""
        return self.areas.get(name)

    def get_areas_at_location(self, world: str, x: float, y: float, z: float) -> List[BuildArea]:
        """Get all build areas containing a specific location"""
        return [area for area in self.areas.values()
                if area.world == world and area.contains_point(x, y, z)]

    def get_player_areas(self, player_name: str, world: str = None) -> List[BuildArea]:
        """Get all build areas where a player is authorized"""
        areas = [area for area in self.areas.values() if area.has_builder(player_name)]
        if world:
            areas = [area for area in areas if area.world == world]
        return areas

    def can_build_at(self, player_name: str, world: str, x: float, y: float, z: float,
                     is_operator: bool = False) -> bool:
        """Check if a player can build at a specific location"""
        # Operators can build anywhere
        if is_operator:
            return True

        # Check if location is in any build area where player is authorized
        areas = self.get_areas_at_location(world, x, y, z)
        return any(area.has_builder(player_name) for area in areas)

    def add_builder_to_area(self, area_name: str, player_name: str) -> bool:
        """Add a builder to a build area"""
        area = self.get_area(area_name)
        if area:
            area.add_builder(player_name)
            self.save_areas()
            return True
        return False

    def remove_builder_from_area(self, area_name: str, player_name: str) -> bool:
        """Remove a builder from a build area"""
        area = self.get_area(area_name)
        if area:
            area.remove_builder(player_name)
            self.save_areas()
            return True
        return False

    def list_areas(self, world: str = None) -> List[BuildArea]:
        """List all build areas, optionally filtered by world"""
        areas = list(self.areas.values())
        if world:
            areas = [area for area in areas if area.world == world]
        return areas

