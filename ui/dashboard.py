"""
Rune AI — Dashboard Content Area

Provides the main content panel on the right side of the application, containing:
- A large heading and subtitle
- A search bar with input field and search button
- Dashboard cards for each feature area (Monsters, Gear, Drops, Travel)
- A recent searches section with placeholder entries

Each card is a reusable widget so new features can be added easily later.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
)
from PySide6.QtCore import Qt


class DashboardCard(QFrame):
    """A single feature card displayed in the dashboard.

    Each card shows a title and description inside a styled panel.
    These are placeholders that will gain functionality later.
    """

    def __init__(self, title: str, description: str, icon: str = "", parent=None):
        super().__init__(parent)

        self.setObjectName("dashboard_card")
        self.setStyleSheet("""
            QFrame#dashboard_card {
                background-color: #1e1e2e;
                border: 1px solid #313244;
                border-radius: 8px;
            }
            QFrame#dashboard_card:hover {
                border-color: #c9a227;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Icon + title row
        header_layout = QHBoxLayout()
        if icon:
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("""
                color: #c9a227;
                font-size: 20px;
                background-color: transparent;
            """)
            header_layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #cdd6f4;
            font-size: 15px;
            font-weight: bold;
            background-color: transparent;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Description text
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            color: #a6adc8;
            font-size: 12px;
            background-color: transparent;
        """)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        layout.addStretch()


class SearchBar(QWidget):
    """A search input field paired with a search button.

    Provides a text box where users can type queries and a styled
    "Search" button to trigger the action (functionality added later).
    """

    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(8)

        # Search input field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.setObjectName("search_input")
        layout.addWidget(self.search_input, stretch=1)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.setObjectName("search_button")
        layout.addWidget(self.search_button)


class RecentSearches(QWidget):
    """A small section listing recent search entries.

    Displays placeholder items for now; actual history will be stored later.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 0)
        layout.setSpacing(6)

        # Section title
        heading = QLabel("Recent Searches")
        heading.setStyleSheet("""
            color: #a6adc8;
            font-size: 12px;
            font-weight: bold;
            background-color: transparent;
        """)
        layout.addWidget(heading)

        # Placeholder entries
        self._entries = ["Vorkath", "Zulrah", "Slayer Tower"]
        for entry in self._entries:
            item = QLabel(f"  {entry}")
            item.setStyleSheet("""
                color: #89b4fa;
                font-size: 13px;
                background-color: transparent;
            """)
            layout.addWidget(item)

        layout.addStretch()


class Dashboard(QWidget):
    """The main content area to the right of the sidebar.

    Assembles the heading, search bar, feature cards, and recent searches
    into a cohesive dashboard layout that fills available space.
    """

    # Feature cards displayed in the dashboard grid
    _CARDS = [
        ("Monsters", "Search OSRS monsters and combat information.", "👹"),
        ("Gear", "Find the best equipment for your target.", "⚙️"),
        ("Drops", "Explore monster drop tables.", "💎"),
        ("Travel", "Find the best ways to reach destinations.", "🗺️"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        self._setup_ui()

    def _setup_ui(self):
        """Build the dashboard layout: heading, search, cards, recent searches."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 16)
        main_layout.setSpacing(16)

        # --- Heading area ---
        self._build_heading(main_layout)

        # --- Search bar ---
        self.search_bar = SearchBar("Search monsters, items, locations...")
        main_layout.addWidget(self.search_bar)

        main_layout.addStretch()  # Push cards and recent searches down slightly

        # --- Dashboard feature cards ---
        self._build_cards(main_layout)

        # --- Recent searches section at the bottom ---
        self.recent_searches = RecentSearches()
        main_layout.addWidget(self.recent_searches)

    def _build_heading(self, parent_layout: QVBoxLayout):
        """Create the large heading and subtitle at the top of the dashboard."""
        title_label = QLabel("Rune AI")
        title_label.setStyleSheet("""
            color: #c9a227;
            font-size: 32px;
            font-weight: bold;
            background-color: transparent;
        """)
        parent_layout.addWidget(title_label)

        subtitle = QLabel("Your OSRS knowledge assistant")
        subtitle.setStyleSheet("""
            color: #a6adc8;
            font-size: 14px;
            background-color: transparent;
        """)
        parent_layout.addWidget(subtitle)

    def _build_cards(self, parent_layout: QVBoxLayout):
        """Create the grid of feature cards."""
        # Horizontal layout to hold two rows of cards side by side
        cards_container = QWidget()
        cards_layout = QVBoxLayout(cards_container)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(12)

        # Split cards into pairs for a 2-column layout
        row_size = 2
        for i in range(0, len(self._CARDS), row_size):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(12)

            for j in range(row_size):
                idx = i + j
                if idx < len(self._CARDS):
                    title, desc, icon = self._CARDS[idx]
                    card = DashboardCard(title, desc, icon)
                    card.setFixedHeight(90)
                    row_layout.addWidget(card, stretch=1)

            cards_layout.addWidget(row_widget)

        parent_layout.addWidget(cards_container)
