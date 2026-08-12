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
            
            # Add drops and locations to monster data
            monster_data["drops"] = drops
            monster_data["locations"] = locations
            
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

        # --- Monster info display area (above buttons) ---
        self.monster_info_container = QWidget()
        self.monster_info_layout = QVBoxLayout(self.monster_info_container)
        self.monster_info_layout.setContentsMargins(0, 0, 0, 0)
        self.monster_info_layout.setSpacing(8)
        
        # Monster name label
        self.monster_name_label = QLabel()
        self.monster_name_label.setStyleSheet("""
            color: #c9a227;
            font-size: 24px;
            font-weight: bold;
            background-color: transparent;
        """)
        self.monster_info_layout.addWidget(self.monster_name_label)
        
        # Monster info labels
        self.combat_level_label = QLabel()
        self.hitpoints_label = QLabel()
        self.attack_style_label = QLabel()
        self.slayer_xp_label = QLabel()
        self.attributes_label = QLabel()
        
        self.monster_info_layout.addWidget(self.combat_level_label)
        self.monster_info_layout.addWidget(self.hitpoints_label)
        self.monster_info_layout.addWidget(self.attack_style_label)
        self.monster_info_layout.addWidget(self.slayer_xp_label)
        self.monster_info_layout.addWidget(self.attributes_label)
        
        # Buttons
        self.button_layout = QHBoxLayout()
        self.drops_button = QPushButton("Drops")
        self.drops_button.setObjectName("drops_button")
        self.locations_button = QPushButton("Locations")
        self.locations_button.setObjectName("locations_button")
        
        self.button_layout.addWidget(self.drops_button)
        self.button_layout.addWidget(self.locations_button)
        
        self.monster_info_layout.addLayout(self.button_layout)
        
        main_layout.addWidget(self.monster_info_container)

        # --- Results display area (scrollable content) ---
        self.results_container = QWidget()
        results_layout = QHBoxLayout(self.results_container)
        results_layout.setContentsMargins(0, 0, 0, 0)
        results_layout.setSpacing(16)

        # Left column for monster text info
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setObjectName("results_display")
        self.text_display.setStyleSheet("""
            QTextEdit#results_display {
                background-color: #1e1e2e;
                border: 1px solid #313244;
                border-radius: 8px;
                color: #cdd6f4;
                font-family: "Segoe UI", "Cascadia Mono", Consolas, monospace;
                font-size: 13px;
            }
        """)
        self.text_display.hide()  # Initially hidden
        results_layout.addWidget(self.text_display, stretch=1)

        # Right column for image placeholders
        self.image_container = QWidget()
        image_layout = QVBoxLayout(self.image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setSpacing(16)

        # Monster image placeholder (square, larger than map)
        self.monster_image_placeholder = QLabel("[ MONSTER IMAGE PLACEHOLDER ]")
        self.monster_image_placeholder.setStyleSheet("""
            background-color: #313244;
            border: 1px solid #414559;
            border-radius: 8px;
            color: #a6adc8;
            font-size: 12px;
            text-align: center;
            min-width: 200px;
            min-height: 200px;
        """)
        self.monster_image_placeholder.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.monster_image_placeholder)

        # Location map placeholder (square)
        self.location_map_placeholder = QLabel("[ LOCATION MAP PLACEHOLDER ]")
        self.location_map_placeholder.setStyleSheet("""
            background-color: #313244;
            border: 1px solid #414559;
            border-radius: 8px;
            color: #a6adc8;
            font-size: 12px;
            text-align: center;
            min-width: 150px;
            min-height: 150px;
        """)
        self.location_map_placeholder.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.location_map_placeholder)

        results_layout.addWidget(self.image_container, stretch=0)

        main_layout.addWidget(self.results_container)

        main_layout.addStretch()  # Push cards and recent searches down slightly



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
        self.text_display.show()
        self.image_container.show()
        
        # Display monster info above buttons
        self._display_monster_info(query, monster_data)
        
        # Initially hide the scrollable content
        self.text_display.hide()
        
        # Connect button signals
        self.drops_button.clicked.connect(lambda: self._show_drops_content(monster_data))
        self.locations_button.clicked.connect(lambda: self._show_location_content(monster_data))
        
    def _display_monster_info(self, query, monster_data):
        """Display monster information above the buttons."""
        self.monster_name_label.setText(monster_data.get("name", query))

        combat_level = monster_data.get("combat1") or monster_data.get("combat") or "N/A"
        self.combat_level_label.setText(f"Combat Level: {combat_level}")

        hitpoints = monster_data.get("hitpoints1") or monster_data.get("hitpoints") or "N/A"
        self.hitpoints_label.setText(f"Hitpoints: {hitpoints}")

        attack_style = monster_data.get("attack style", "N/A")
        self.attack_style_label.setText(f"Attack Style: {attack_style}")

        slayer_xp = monster_data.get("slayxp1") or monster_data.get("slayxp") or "N/A"
        self.slayer_xp_label.setText(f"Slayer XP: {slayer_xp}")

        attributes = monster_data.get("attributes", "N/A")
        if isinstance(attributes, str):
            attributes = ", ".join(attr.strip().capitalize() for attr in attributes.split(","))
        self.attributes_label.setText(f"Attributes: {attributes}")
        
    def _show_drops_content(self, monster_data):
        """Display drops grouped by category."""
        drops = monster_data.get("drops", [])
        if not drops:
            self.text_display.setText("No drops information available.")
            self.text_display.show()
            return
        groups = {}
        for drop in drops:
            category = drop.get("category", "Uncategorized")
            groups.setdefault(category, []).append(drop)
        lines = ["DROPS", ""]
        for category, items in groups.items():
            lines.append(category.upper())
            for drop in items:
                name = drop.get("name", "Unknown")
                quantity = drop.get("quantity", "N/A")
                rarity = drop.get("rarity", "N/A")
                lines.append(f"  {name}    x{quantity}    {rarity}")
            lines.append("")
        self.text_display.setPlainText("\n".join(lines))
        self.text_display.show()

    def _show_location_content(self, monster_data):
        """Display locations content in the scrollable area."""
        locations = monster_data.get("locations", [])
        if not locations:
            content = "No location information available."
        else:
            content = "\n".join([f"- {location}" for location in locations])
        
        self.text_display.setText(content)
        self.text_display.show()        

        
    def show_monsters_view(self):
        """Show the monster search interface."""
        # Make the search bar and results display visible
        self.search_bar.show()
        self.text_display.show()
        self.image_container.show()