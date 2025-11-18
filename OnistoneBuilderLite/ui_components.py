"""UI components using server-ui for OnistoneBuilderLite."""

from typing import TYPE_CHECKING, Callable, List, Optional, Any
from server_ui import ModalForm, ActionForm, MessageForm

if TYPE_CHECKING:
    from endstone.player import Player


class UIBuilder:
    """Helper class for building UI forms."""
    
    @staticmethod
    def create_main_menu(player: "Player") -> ActionForm:
        """Create main builder menu.
        
        Args:
            player: Player to show menu to
            
        Returns:
            ActionForm for main menu
        """
        form = ActionForm()
        form.title("§l§6Onistone Builder§r")
        form.content("§7Select an action:§r")
        
        form.button("§2Selection§r\n§7Set positions§r", icon="textures/ui/icon_recipe_item")
        form.button("§3Clipboard§r\n§7Copy/Cut/Paste§r", icon="textures/ui/icon_book_writable")
        form.button("§5Blueprints§r\n§7Save/Load§r", icon="textures/ui/icon_book_portfolio")
        form.button("§6Builder Zones§r\n§7Manage zones§r", icon="textures/ui/icon_deals")
        form.button("§eUndo§r\n§7Undo last action§r", icon="textures/ui/icon_undo")
        form.button("§cClose§r", icon="textures/ui/icon_cancel")
        
        return form
    
    @staticmethod
    def create_selection_menu(player: "Player", has_selection: bool, selection_info: str) -> ActionForm:
        """Create selection menu.
        
        Args:
            player: Player to show menu to
            has_selection: Whether player has active selection
            selection_info: Selection information text
            
        Returns:
            ActionForm for selection menu
        """
        form = ActionForm()
        form.title("§l§2Selection§r")
        form.content(f"§7Current Selection:§r\n{selection_info}")
        
        form.button("§aSet Position 1§r\n§7At current location§r", icon="textures/ui/icon_best3")
        form.button("§aSet Position 2§r\n§7At current location§r", icon="textures/ui/icon_best3")
        
        if has_selection:
            form.button("§cClear Selection§r", icon="textures/ui/icon_cancel")
        
        form.button("§7« Back§r", icon="textures/ui/icon_back")
        
        return form
    
    @staticmethod
    def create_clipboard_menu(player: "Player", clipboard_count: int) -> ActionForm:
        """Create clipboard menu.
        
        Args:
            player: Player to show menu to
            clipboard_count: Number of clipboard entries
            
        Returns:
            ActionForm for clipboard menu
        """
        form = ActionForm()
        form.title("§l§3Clipboard§r")
        form.content(f"§7Clipboard entries: §e{clipboard_count}§r")
        
        form.button("§2Copy Selection§r\n§7Copy to clipboard§r", icon="textures/ui/icon_book_writable")
        form.button("§6Cut Selection§r\n§7Cut to clipboard§r", icon="textures/ui/icon_book_writable")
        form.button("§5Paste§r\n§7Paste from clipboard§r", icon="textures/ui/icon_book_portfolio")
        form.button("§eBrowse Clipboard§r\n§7View all entries§r", icon="textures/ui/icon_book_portfolio")
        form.button("§7« Back§r", icon="textures/ui/icon_back")
        
        return form
    
    @staticmethod
    def create_paste_options_form() -> ModalForm:
        """Create paste options form.
        
        Returns:
            ModalForm for paste options
        """
        form = ModalForm()
        form.title("§l§5Paste Options§r")
        
        form.dropdown("Rotation:", ["0°", "90°", "180°", "270°"], default=0)
        form.toggle("Flip X", default=False)
        form.toggle("Flip Y", default=False)
        form.toggle("Flip Z", default=False)
        form.slider("Offset X:", -64, 64, step=1, default=0)
        form.slider("Offset Y:", -64, 64, step=1, default=0)
        form.slider("Offset Z:", -64, 64, step=1, default=0)
        form.toggle("Place Air Blocks", default=True)
        form.toggle("Ignore Liquids", default=False)
        
        return form
    
    @staticmethod
    def create_blueprint_menu(player: "Player", blueprints: List[str]) -> ActionForm:
        """Create blueprint menu.
        
        Args:
            player: Player to show menu to
            blueprints: List of blueprint names
            
        Returns:
            ActionForm for blueprint menu
        """
        form = ActionForm()
        form.title("§l§5Blueprints§r")
        form.content(f"§7Available blueprints: §e{len(blueprints)}§r")
        
        form.button("§2Save Blueprint§r\n§7Save clipboard§r", icon="textures/ui/icon_book_writable")
        form.button("§3Load Blueprint§r\n§7Load to clipboard§r", icon="textures/ui/icon_book_portfolio")
        form.button("§eBrowse Blueprints§r\n§7View all§r", icon="textures/ui/icon_book_portfolio")
        form.button("§6Shared Blueprints§r\n§7Community§r", icon="textures/ui/icon_deals")
        form.button("§7« Back§r", icon="textures/ui/icon_back")
        
        return form
    
    @staticmethod
    def create_zone_menu(player: "Player", zones: List[str]) -> ActionForm:
        """Create zone menu.
        
        Args:
            player: Player to show menu to
            zones: List of zone names
            
        Returns:
            ActionForm for zone menu
        """
        form = ActionForm()
        form.title("§l§6Builder Zones§r")
        form.content(f"§7Your zones: §e{len(zones)}§r")
        
        form.button("§2Create Zone Here§r\n§7Temporary zone§r", icon="textures/ui/icon_best3")
        form.button("§3My Zones§r\n§7View all zones§r", icon="textures/ui/icon_book_portfolio")
        form.button("§eShare Zone§r\n§7Add builders§r", icon="textures/ui/icon_deals")
        form.button("§7« Back§r", icon="textures/ui/icon_back")
        
        return form
    
    @staticmethod
    def create_confirm_dialog(title: str, message: str) -> MessageForm:
        """Create confirmation dialog.
        
        Args:
            title: Dialog title
            message: Dialog message
            
        Returns:
            MessageForm for confirmation
        """
        form = MessageForm()
        form.title(title)
        form.content(message)
        form.button1("§aConfirm§r")
        form.button2("§cCancel§r")
        
        return form
    
    @staticmethod
    def create_input_form(title: str, label: str, placeholder: str = "") -> ModalForm:
        """Create simple input form.
        
        Args:
            title: Form title
            label: Input label
            placeholder: Input placeholder
            
        Returns:
            ModalForm for input
        """
        form = ModalForm()
        form.title(title)
        form.text_input(label, placeholder=placeholder)
        
        return form

