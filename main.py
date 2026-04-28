import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QSplitter, QVBoxLayout
from diceClass import *
from views import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Background
        self.setStyleSheet("""
                            QMainWindow {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 #0d0d0d, stop: 1 #1c1c1c
        );
        color: white;
    }
                           """)

        self.setWindowTitle("John DnD")

        # Set the central widget of the Window.
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Dice View
        dice = DiceView()

        def on_settings_opened(settings_view: SettingsView):
            settings_view.dice_body_color_changed.connect(dice.dice.set_body_color)
            settings_view.dice_edge_color_changed.connect(dice.dice.set_edge_color)
            settings_view.dice_number_color_changed.connect(dice.dice.set_num_color)
            settings_view.inner_triangle_toggled.connect(dice.dice.set_show_triangle)
            settings_view.default_die_changed.connect(dice.dice.set_dice)


        # Sidebar View
        sidebar = SidebarView(on_open_settings=on_settings_opened)

        # Character Sheet View
        characterSheet = CharacterSheetView()

        # Dice Multipliers/stats view (?)
        multipliers = MultiplierView()

        dice.roll_completed.connect(multipliers.on_roll_completed)

         # Right side splits
        right_side = QSplitter(Qt.Orientation.Vertical)
        right_side.addWidget(dice)
        right_side.addWidget(multipliers)
        right_side.setSizes([600, 600])

        main_view = QSplitter(Qt.Orientation.Horizontal)
        main_view.addWidget(sidebar)
        main_view.addWidget(characterSheet)
        main_view.addWidget(right_side)
        main_view.setSizes([85, 400, 600])

        layout.addWidget(main_view)

    
    


app = QApplication(sys.argv)

window = MainWindow()
window.showMaximized()

app.exec()