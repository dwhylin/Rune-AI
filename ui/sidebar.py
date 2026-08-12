"""
Rune AI — Sidebar Navigation

Provides a left-side navigation panel with branded title and clickable menu items.
Each button responds to hover and shows the currently selected page with a gold accent.

The sidebar is a reusable QFrame that can be placed inside any layout.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)
from PySide6.QtCore import Qt, Signal


class Sidebar(QFrame):
    """Left navigation sidebar with menu items and branding."""

    # Menu items displayed in the sidebar (icon placeholder + label)
    _MENU_ITEMS = [
        ("⚔", "Home"),
        ("👹", "Monsters"),
        ("⚙️", "Gear"),
        ("💎", "Drops"),
        ("🗺️", "Travel"),
        ("📖", "Wiki"),
    ]

    # Signal to emit when a page is selected
    page_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Sidebar dimensions and styling
        self.setFixedWidth(220)
        self.setObjectName("sidebar")
        self.setStyleSheet("""
            QFrame#sidebar {
                background-color: #181825;
                border-right: 1px solid #313244;
                border-radius: 0;
            }
        """)

        self._selected_page = "Home"  # Track which page is currently active
        self._buttons = {}             # Map page names to their QPushButton objects

        self._setup_ui()

    def _setup_ui(self):
        """Build the sidebar layout: logo, menu items, settings."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 12)
        layout.setSpacing(4)

        # --- Branded title area at the top ---
        self._build_logo(layout)

        layout.addStretch()  # Pushes remaining items downward

        # --- Navigation menu items ---
        for icon, label in self._MENU_ITEMS:
            btn = QPushButton(f"{icon}  {label}")
            btn.setObjectName("sidebar_button")
            btn.setCheckable(True)  # Allows toggling checked state
            btn.clicked.connect(lambda checked, l=label: self._on_page_selected(l))
            layout.addWidget(btn)
            self._buttons[label] = btn

        layout.addStretch()  # Pushes settings to the very bottom

        # --- Settings button at the bottom ---
        settings_btn = QPushButton("⚙️  Settings")
        settings_btn.setObjectName("sidebar_settings")
        layout.addWidget(settings_btn)

        # Set Home as the initially selected page
        self._on_page_selected("Home")

    def _build_logo(self, parent_layout: QVBoxLayout):
        """Create the Rune AI logo/title at the top of the sidebar."""
        logo_frame = QFrame()
        logo_layout = QHBoxLayout(logo_frame)
        logo_layout.setContentsMargins(4, 0, 4, 8)

        # Rune icon placeholder
        icon_label = QLabel("⚔")
        icon_label.setStyleSheet("""
            color: #c9a227;
            font-size: 26px;
            background-color: transparent;
        """)
        logo_layout.addWidget(icon_label)

        # App name
        title_text = QLabel("Rune AI")
        title_text.setObjectName("title_label")
        logo_layout.addWidget(title_text)

        logo_layout.addStretch()
        parent_layout.addWidget(logo_frame)

    def _on_page_selected(self, page_name: str):
        """Handle a menu item being clicked.

        Unchecks all buttons and checks only the selected one so that
        exactly one page appears highlighted at any time.
        """
        self._selected_page = page_name
        for label, btn in self._buttons.items():
            btn.setChecked(label == page_name)
        
        # Emit signal when a page is selected
        self.page_selected.emit(page_name)

    @property
    def selected_page(self):
        """Return the name of the currently selected navigation page."""
        return self._selected_page
