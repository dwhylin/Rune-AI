"""
Rune AI — Main Window

Defines the MainWindow class: the primary window that users see when they
launch Rune AI. It combines a left navigation sidebar with a main content
dashboard area, forming the core interface of the application.

As features are added later, each sidebar item will swap in its own
content panel while keeping the sidebar and overall layout intact.
"""

from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QStatusBar, QWidget
from ui.sidebar import Sidebar
from ui.dashboard import Dashboard


class MainWindow(QMainWindow):
    """The main application window for Rune AI."""

    def __init__(self):
        super().__init__()

        # Window properties — desktop-friendly default size
        self.setWindowTitle("Rune AI")
        self.resize(1050, 700)
        self.setMinimumSize(800, 550)

        # Build the UI
        self._setup_ui()

    def _setup_ui(self):
        """Assemble the sidebar and dashboard into a horizontal layout."""
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left side: navigation sidebar (~220px wide)
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # Right side: main content dashboard
        self.dashboard = Dashboard()
        main_layout.addWidget(self.dashboard, stretch=1)

        # Connect sidebar signal to handle page changes
        self.sidebar.page_selected.connect(self._on_sidebar_page_selected)

        # Status bar at the bottom of the window
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready — Rune AI v0.1")

    def _on_sidebar_page_selected(self, page_name: str):
        """Handle sidebar page selection."""
        # For now, only handle Monsters page - others can be implemented later
        if page_name == "Monsters":
            # This will show the monsters search functionality
            self.dashboard.show_monsters_view()
        else:
            # For other pages, we could implement different views
            pass
