"""Permission management for OnistoneBuilderLite."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from endstone.command import CommandSender
    from endstone.player import Player


class Permissions:
    """Manages permission checks for the plugin."""
    
    BASE = "onistone.builder"
    
    # Core permissions
    MENU = f"{BASE}.menu"
    SELECT = f"{BASE}.select"
    COPY = f"{BASE}.copy"
    CUT = f"{BASE}.cut"
    PASTE = f"{BASE}.paste"
    
    # Blueprint permissions
    BLUEPRINT_SAVE = f"{BASE}.blueprint.save"
    BLUEPRINT_SHARED = f"{BASE}.blueprint.shared"
    BLUEPRINT_PUBLISH = f"{BASE}.blueprint.publish"
    
    # Zone permissions
    ZONE = f"{BASE}.zone"
    BYPASS_ZONE = f"{BASE}.bypass.zone"
    
    # Advanced permissions
    INVENTORY_COPY = f"{BASE}.inventory.copy"
    ENTITY_COPY = f"{BASE}.entity.copy"
    
    # Admin permissions
    ADMIN = f"{BASE}.admin"
    
    @staticmethod
    def has_permission(sender: "CommandSender", permission: str) -> bool:
        """Check if sender has permission.
        
        Args:
            sender: Command sender to check
            permission: Permission node to check
            
        Returns:
            True if sender has permission
        """
        # Operators have all permissions
        if hasattr(sender, "is_op") and sender.is_op:
            return True
        
        # Check specific permission
        return sender.has_permission(permission)
    
    @staticmethod
    def has_any(sender: "CommandSender", *permissions: str) -> bool:
        """Check if sender has any of the given permissions.
        
        Args:
            sender: Command sender to check
            *permissions: Permission nodes to check
            
        Returns:
            True if sender has any permission
        """
        if hasattr(sender, "is_op") and sender.is_op:
            return True
        
        return any(sender.has_permission(perm) for perm in permissions)
    
    @staticmethod
    def has_all(sender: "CommandSender", *permissions: str) -> bool:
        """Check if sender has all of the given permissions.
        
        Args:
            sender: Command sender to check
            *permissions: Permission nodes to check
            
        Returns:
            True if sender has all permissions
        """
        if hasattr(sender, "is_op") and sender.is_op:
            return True
        
        return all(sender.has_permission(perm) for perm in permissions)
    
    @staticmethod
    def get_all_permissions() -> list[str]:
        """Get list of all permission nodes.
        
        Returns:
            List of all permission nodes
        """
        return [
            Permissions.MENU,
            Permissions.SELECT,
            Permissions.COPY,
            Permissions.CUT,
            Permissions.PASTE,
            Permissions.BLUEPRINT_SAVE,
            Permissions.BLUEPRINT_SHARED,
            Permissions.BLUEPRINT_PUBLISH,
            Permissions.ZONE,
            Permissions.BYPASS_ZONE,
            Permissions.INVENTORY_COPY,
            Permissions.ENTITY_COPY,
            Permissions.ADMIN,
        ]
    
    @staticmethod
    def format_permission_error(permission: str) -> str:
        """Format permission error message.
        
        Args:
            permission: Permission that was missing
            
        Returns:
            Formatted error message
        """
        return f"§cYou don't have permission: §e{permission}§r"

