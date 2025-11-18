"""Storage utilities for OnistoneBuilderLite."""

import json
import struct
import zlib
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional
from datetime import datetime


class BlockData:
    """Represents a block with its type and state."""
    
    def __init__(self, block_type: str, data: int = 0, nbt: Optional[Dict] = None):
        """Initialize block data.
        
        Args:
            block_type: Block type identifier
            data: Block data value
            nbt: Optional NBT data
        """
        self.block_type = block_type
        self.data = data
        self.nbt = nbt or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"type": self.block_type, "data": self.data}
        if self.nbt:
            result["nbt"] = self.nbt
        return result
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "BlockData":
        """Create from dictionary."""
        return BlockData(
            data.get("type", "minecraft:air"),
            data.get("data", 0),
            data.get("nbt")
        )
    
    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if not isinstance(other, BlockData):
            return False
        return (self.block_type == other.block_type and 
                self.data == other.data)
    
    def __hash__(self) -> int:
        """Get hash."""
        return hash((self.block_type, self.data))


class RLECompressor:
    """Run-Length Encoding compressor for block data."""
    
    @staticmethod
    def compress(blocks: List[BlockData]) -> bytes:
        """Compress block list using RLE.
        
        Args:
            blocks: List of blocks to compress
            
        Returns:
            Compressed bytes
        """
        if not blocks:
            return b""
        
        # Build palette
        palette: List[BlockData] = []
        palette_map: Dict[BlockData, int] = {}
        
        for block in blocks:
            if block not in palette_map:
                palette_map[block] = len(palette)
                palette.append(block)
        
        # RLE encode palette indices
        rle_data: List[Tuple[int, int]] = []  # (palette_index, count)
        current_idx = palette_map[blocks[0]]
        count = 1
        
        for block in blocks[1:]:
            idx = palette_map[block]
            if idx == current_idx:
                count += 1
            else:
                rle_data.append((current_idx, count))
                current_idx = idx
                count = 1
        rle_data.append((current_idx, count))
        
        # Serialize
        data = {
            "palette": [b.to_dict() for b in palette],
            "rle": rle_data
        }
        
        json_bytes = json.dumps(data).encode("utf-8")
        return zlib.compress(json_bytes)
    
    @staticmethod
    def decompress(data: bytes) -> List[BlockData]:
        """Decompress RLE data to block list.
        
        Args:
            data: Compressed bytes
            
        Returns:
            List of blocks
        """
        if not data:
            return []
        
        json_bytes = zlib.decompress(data)
        obj = json.loads(json_bytes.decode("utf-8"))
        
        # Rebuild palette
        palette = [BlockData.from_dict(b) for b in obj["palette"]]
        
        # Decode RLE
        blocks: List[BlockData] = []
        for idx, count in obj["rle"]:
            blocks.extend([palette[idx]] * count)
        
        return blocks


class BlueprintMetadata:
    """Metadata for a blueprint."""
    
    def __init__(self, name: str, description: str = "", author: str = ""):
        """Initialize metadata.
        
        Args:
            name: Blueprint name
            description: Blueprint description
            author: Blueprint author
        """
        self.name = name
        self.description = description
        self.author = author
        self.created_at = datetime.now().isoformat()
        self.dimensions: Tuple[int, int, int] = (0, 0, 0)
        self.block_count = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "createdAt": self.created_at,
            "dimensions": self.dimensions,
            "blockCount": self.block_count,
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "BlueprintMetadata":
        """Create from dictionary."""
        meta = BlueprintMetadata(
            data.get("name", "Unnamed"),
            data.get("description", ""),
            data.get("author", "")
        )
        meta.created_at = data.get("createdAt", meta.created_at)
        meta.dimensions = tuple(data.get("dimensions", (0, 0, 0)))
        meta.block_count = data.get("blockCount", 0)
        return meta

