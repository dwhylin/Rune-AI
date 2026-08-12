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
    QTextEdit,
)
from PySide6.QtCore import Qt, Signal
import json


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

    # Signal to emit when search is completed
    search_completed = Signal(str, dict)
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

        # Connect the search button to a handler
        self.search_button.clicked.connect(self._on_search_clicked)
        
        # Also connect Enter key press in the input field
        self.search_input.returnPressed.connect(self._on_search_clicked)

    def _on_search_clicked(self):
        """Handle search button click or Enter key press."""
        # Get text from input field
        query = self.search_input.text().strip()
        if not query:
            return
        
        # Import the monster parser here to avoid circular imports
        try:
            from wiki.monsters import fetch_raw_wikitext, extract_infobox_monster, extract_loc_lines, get_parsed_drops
            
            # Fetch and parse the wikitext
            wikitext = fetch_raw_wikitext(query)
            if not wikitext:
                print(f"Failed to fetch wikitext for {query}")
                return
            
            # Extract data
            monster_data = extract_infobox_monster(wikitext)
            locations = extract_loc_lines(wikitext)
            drops = get_parsed_drops(wikitext)
            
            # Add drops to monster data
            monster_data["drops"] = drops
            
            # Emit signal with parsed data (to be handled by the parent)
            self.search_completed.emit(query, monster_data)
        except Exception as e:
            print(f"Error parsing {query}: {e}")


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
        
        # Connect search signal to display results
        self.search_bar.search_completed.connect(self._on_search_completed)

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

        # --- Results display area ---
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setObjectName("results_display")
        self.results_display.setStyleSheet("""
            QTextEdit#results_display {
                background-color: #1e1e2e;
                border: 1px solid #313244;
                border-radius: 8px;
                color: #cdd6f4;
                font-family: "Segoe UI", "Cascadia Mono", Consolas, monospace;
                font-size: 13px;
            }
        """)
        self.results_display.hide()  # Initially hidden
        main_layout.addWidget(self.results_display)

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

    def _on_search_completed(self, query, monster_data):
        """Handle search completion and display results in GUI."""
        # Show the results area
        self.results_display.show()
        
        # Format the monster data for display
        formatted_result = self._format_monster_data(query, monster_data)
        self.results_display.setPlainText(formatted_result)
        
    def _format_monster_data(self, query, monster_data):
        """Format monster data for display in GUI."""
        result = []
        result.append(f"Monster: {query}")
        result.append("")
        
        # Add basic monster info if available
        if "combat_level" in monster_data:
            result.append(f"Combat Level: {monster_data['combat_level']}")
        if "hitpoints" in monster_data:
            result.append(f"Hitpoints: {monster_data['hitpoints']}")
        if "attack_style" in monster_data:
            result.append(f"Attack Style: {monster_data['attack_style']}")
        if "max_hit" in monster_data:
            result.append(f"Max Hit: {monster_data['max_hit']}")
        if "attributes" in monster_data:
            # Handle attributes as comma-separated string instead of character-by-character
            if isinstance(monster_data['attributes'], list):
                result.append(f"Attributes: {', '.join(monster_data['attributes'])}")
            else:
                # If it's a comma-separated string, split and capitalize each word
                if isinstance(monster_data['attributes'], str):
                    attributes_list = [attr.strip().capitalize() for attr in monster_data['attributes'].split(',')]
                    result.append(f"Attributes: {', '.join(attributes_list)}")
                else:
                    result.append(f"Attributes: {monster_data['attributes']}")
        if "slayer_xp" in monster_data:
            result.append(f"Slayer XP: {monster_data['slayer_xp']}")
        if "weakness" in monster_data:
            # Handle weakness as comma-separated string
            if isinstance(monster_data['weakness'], list):
                result.append(f"Weakness: {', '.join(monster_data['weakness'])}")
            else:
                result.append(f"Weakness: {monster_data['weakness']}")
        if "immunities" in monster_data:
            # Handle immunities as comma-separated string
            if isinstance(monster_data['immunities'], list):
                result.append(f"Immunities: {', '.join(monster_data['immunities'])}")
            else:
                result.append(f"Immunities: {monster_data['immunities']}")
        
        # Add locations
        if "locations" in monster_data:
            result.append("")
            result.append("Locations:")
            for loc in monster_data["locations"]:
                result.append(f"  {loc}")
        
        # Add drops
        if "drops" in monster_data and monster_data["drops"]:
            result.append("")
            result.append("Drops:")
            
            # Group drops by category
            categories = {}
            for drop in monster_data["drops"]:
                category = drop.get("category", "Unknown")
                if category not in categories:
                    categories[category] = []
                categories[category].append(drop)
            
            # Sort and display categories
            sorted_categories = sorted(categories.keys())
            for category in sorted_categories:
                drops_in_category = categories[category]
                
                # Add category header
                result.append(f"  {category}")
                
                # Group by rarity for better formatting
                rarity_groups = {}
                for drop in drops_in_category:
                    rarity = drop.get("rarity", "N/A")
                    if rarity not in rarity_groups:
                        rarity_groups[rarity] = []
                    rarity_groups[rarity].append(drop)
                
                # Display each drop with proper formatting
                for rarity, drops in rarity_groups.items():
                    # Special handling for Brimstone key - show as 1/50
                    if any("Brimstone" in drop.get("name", "") or "brimstone" in drop.get("name", "").lower() for drop in drops):
                        rarity = "1/50"
                    
                    # Display all drops with this rarity
                    for drop in drops:
                        name = drop.get("name", "N/A")
                        quantity = drop.get("quantity", "N/A")
                        
                        # Handle Brimstone key specifically
                        if "Brimstone" in name or "brimstone" in name.lower():
                            rarity = "1/50"
                        
                        result.append(f"    {name} - {quantity} - {rarity}")
        
        return "\n".join(result)
        
    def show_monsters_view(self):
        """Show the monster search interface."""
        # Make the search bar and results display visible
        self.search_bar.show()
        self.results_display.show()

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
