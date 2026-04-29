import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QSplitter, QVBoxLayout
from diceClass import *
from views import *
import json, os

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
            settings_view.dice_body_color_changed.connect(dice.apply_accent)
            settings_view.dice_body_color_changed.connect(characterSheet.apply_accent)
            settings_view.dice_body_color_changed.connect(multipliers.apply_accent)


        # Sidebar View
        sidebar = SidebarView(on_open_settings=on_settings_opened)

        # Character Sheet View
        characterSheet = CharacterSheetView()
        self.characterSheet = characterSheet

        # Dice Multipliers/stats view (?)
        multipliers = MultiplierView()
        self.multipliers = multipliers

        self.dice = dice
        self._load_settings()

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
    
    def closeEvent(self, event):
        d = self.dice.dice  # DiceWidget
        settings = {
            "dice_type":   d.dice_type,
            "body_color":  d.body_color.name(),
            "edge_color":  d.edge_color.name(),
            "num_color":   d.num_color.name(),
            "show_triangle": d.show_triangle,
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=2)
        event.accept()
    
    def _load_settings(self):
        if not os.path.exists("settings.json"):
            return
        with open("settings.json") as f:
            s = json.load(f)
        d = self.dice.dice
        if "body_color" in s:
            color = QColor(s["body_color"])
            d.set_body_color(color)
            self.dice.apply_accent(color)
            self.characterSheet.apply_accent(color)
            self.multipliers.apply_accent(color)
        if "edge_color"  in s: d.set_edge_color(QColor(s["edge_color"]))
        if "num_color"   in s: d.set_num_color(QColor(s["num_color"]))
        if "show_triangle" in s: d.set_show_triangle(s["show_triangle"])
        if "dice_type"   in s:
            d.set_dice(s["dice_type"])
            self.dice.dice_select.setCurrentText(f"d{s['dice_type']}")
    
    


app = QApplication(sys.argv)

window = MainWindow()
window.showMaximized()

app.exec()