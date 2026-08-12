"""
Rune AI — Application Setup

Creates the QApplication instance (the heart of every Qt application),
applies a dark theme with gold accents inspired by OSRS, and shows the
main window before starting the event loop that handles user input and rendering.
"""

import sys
from PySide6.QtWidgets import QApplication
from data.database import init_database
from ui.main_window import MainWindow


def run():
    """Create the app, apply styling, show the window, and start the event loop."""
    # In PySide6/Qt6, high-DPI scaling is enabled by default — no extra setup needed.
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Cross-platform dark-capable style engine

    # Initialize the SQLite database (creates data/runeai.db if missing)
    init_database()

    # Apply our custom dark theme with gold accents
    _apply_dark_theme(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


def _apply_dark_theme(app: QApplication):
    """Apply a dark, modern stylesheet to every widget in the app.

    Uses a dark background (#1e1e2e) with subtle contrast panels and gold/yellow
    accent colors inspired by Old School RuneScape's aesthetic.
    """
    app.setStyleSheet("""
        /* ---------- Base palette ---------- */
        QMainWindow {
            background-color: #1e1e2e;
        }

        QWidget {
            color: #cdd6f4;
            background-color: transparent;
            font-family: "Segoe UI", "Cascadia Mono", Consolas, monospace;
            font-size: 13px;
        }

        /* ---------- Main window frame ---------- */
        QMainWindow > QFrame {
            background-color: #1e1e2e;
            border-radius: 8px;
        }

        /* ---------- Title labels ---------- */
        QLabel#title_label {
            color: #c9a227;
            font-size: 18px;
            font-weight: bold;
            background-color: transparent;
        }

        QLabel#subtitle_label {
            color: #a6adc8;
            font-size: 12px;
            background-color: transparent;
        }

        /* ---------- Central area panels ---------- */
        QFrame#central_panel {
            background-color: #181825;
            border-radius: 6px;
            border: 1px solid #313244;
        }

        QLabel#welcome_label {
            color: #cdd6f4;
            font-size: 15px;
            background-color: transparent;
        }

        /* ---------- Sidebar buttons ---------- */
        QPushButton#sidebar_button {
            background-color: transparent;
            border: none;
            text-align: left;
            padding: 10px 16px;
            color: #a6adc8;
            font-size: 14px;
            border-radius: 6px;
        }

        QPushButton#sidebar_button:hover {
            background-color: #313244;
            color: #cdd6f4;
        }

        QPushButton#sidebar_button:checked {
            background-color: #313244;
            color: #c9a227;
            font-weight: bold;
        }

        QPushButton#sidebar_settings {
            background-color: transparent;
            border: none;
            text-align: left;
            padding: 10px 16px;
            color: #a6adc8;
            font-size: 14px;
            border-radius: 6px;
        }

        QPushButton#sidebar_settings:hover {
            background-color: #313244;
            color: #cdd6f4;
        }

        /* ---------- Main content buttons (search) ---------- */
        QPushButton#search_button {
            background-color: #c9a227;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            color: #1e1e2e;
            font-weight: bold;
            font-size: 14px;
        }

        QPushButton#search_button:hover {
            background-color: #d4ad3a;
        }

        QPushButton#search_button:pressed {
            background-color: #b89020;
        }

        /* ---------- Text inputs (search box) ---------- */
        QLineEdit {
            background-color: #1e1e2e;
            border: 1px solid #45475a;
            border-radius: 6px;
            padding: 8px 12px;
            color: #cdd6f4;
            font-size: 14px;
        }

        QLineEdit:focus {
            border-color: #c9a227;
        }

        /* ---------- Scroll areas ---------- */
        QScrollBar:vertical {
            background-color: #1e1e2e;
            width: 8px;
            border-radius: 4px;
        }

        QScrollBar::handle:vertical {
            background-color: #45475a;
            border-radius: 4px;
            min-height: 30px;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0;
        }

        /* ---------- Status bar ---------- */
        QStatusBar {
            background-color: #181825;
            color: #a6adc8;
            border-top: 1px solid #313244;
        }

        QStatusBar QLabel {
            color: #a6adc8;
        }
    """)