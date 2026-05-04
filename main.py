import sys
 
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QSplitter, QVBoxLayout
from diceClass import *
import views
from views import *
import json, os
 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
 
        # Linear Background Style
        self.setStyleSheet("""
                            QMainWindow {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 #0d0d0d, stop: 1 #1c1c1c
        );
        color: white;
    }
                           """)
 
        self.setWindowTitle("John D&D")
        self._campaign_name = ""
 
        # Set the central widget of the Window.
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
 
        # Dice View
        dice = DiceView()

        # function to latch on to signals from settings_view
        def on_settings_opened(settings_view: SettingsView):
            settings_view.dice_body_color_changed.connect(dice.dice.set_body_color)
            settings_view.dice_edge_color_changed.connect(dice.dice.set_edge_color)
            settings_view.dice_number_color_changed.connect(dice.dice.set_num_color)
            settings_view.inner_triangle_toggled.connect(dice.dice.set_show_triangle)
            settings_view.default_die_changed.connect(dice.dice.set_dice)
            settings_view.dice_body_color_changed.connect(dice.apply_accent)
            settings_view.dice_body_color_changed.connect(characterSheet.apply_accent)
            settings_view.dice_body_color_changed.connect(multipliers.apply_accent)
            settings_view.dice_body_color_changed.connect(self.sidebar.apply_accent)
            settings_view.campaign_input.setText(self._campaign_name)
            settings_view.campaign_name_changed.connect(self._update_title)

 
        # Character Sheet View
        characterSheet = CharacterSheetView()
 
        #side bar view pass the character sheet through so it can use its functions
        self.sidebar = SidebarView(characterSheet, on_open_settings=on_settings_opened)
        self.characterSheet = characterSheet
 
        # Dice Multipliers/stats view 
        multipliers = MultiplierView()
        self.multipliers = multipliers

        # init dice class for some functions
        self.dice = dice

        # load settings on launch
        self._load_settings()
 
        # Connections to change multiplier view on roll and when character sheet updates
        dice.roll_completed.connect(multipliers.on_roll_completed)
        characterSheet.character_changed.connect(multipliers.update_mods)
 
         # Right side splits
        right_side = QSplitter(Qt.Orientation.Vertical)
        right_side.addWidget(dice)
        right_side.addWidget(multipliers)
        right_side.setSizes([600, 600])

        # Main splits
        main_view = QSplitter(Qt.Orientation.Horizontal)
        main_view.addWidget(self.sidebar)
        main_view.addWidget(characterSheet)
        main_view.addWidget(right_side)
        main_view.setSizes([85, 400, 600])
 
        layout.addWidget(main_view)

    # Script to update the window title with the name of the Campaign
    def _update_title(self, name: str):
        self._campaign_name = name.strip()
        if name.strip():
            self.setWindowTitle(f"John DnD — {name.strip()}")
        else:
            self.setWindowTitle("John D&D")
    
    # A script that runs on closing of the application, saves the state of the window as JSON
    def closeEvent(self, event):
        d = self.dice.dice 
        settings = {
            "dice_type":     d.dice_type,
            "body_color":    d.body_color.name(),
            "edge_color":    d.edge_color.name(),
            "num_color":     d.num_color.name(),
            "show_triangle": d.show_triangle,
            "campaign_name": self._campaign_name,
            "characters": [
                {
                    "name":         c.name,
                    "clas":         c.clas,
                    "race":         c.race,
                    "strength":     c.strength,
                    "dexterity":    c.dexterity,
                    "constitution": c.constitution,
                    "intel":        c.intel,
                    "wisdom":       c.wisdom,
                    "char":         c.charisma,
                    "lore":         c.lore,
                    "notes":        c.notes,
                }
                for c in views.char_list
            ],
            "current_char_index": views.char_list.index(views.current_char) if views.current_char in views.char_list else -1,
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=2)
        event.accept()
    
    # Loads the settings upon opening and loads the settings into the widgets/views
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
        if "edge_color"    in s: d.set_edge_color(QColor(s["edge_color"]))
        if "num_color"     in s: d.set_num_color(QColor(s["num_color"]))
        if "show_triangle" in s: d.set_show_triangle(s["show_triangle"])
        if "dice_type"     in s:
            d.set_dice(s["dice_type"])
            self.dice.dice_select.setCurrentText(f"d{s['dice_type']}")
 
        # Restore saved characters
        if "characters" in s:
            character_layout = self.sidebar._character_layout
 
            for char_data in s["characters"]:
                obj = Character()
                obj.name         = char_data["name"]
                obj.clas         = char_data["clas"]
                obj.race         = char_data["race"]
                obj.strength     = int(char_data["strength"])
                obj.dexterity    = int(char_data["dexterity"])
                obj.constitution = int(char_data["constitution"])
                obj.intel        = int(char_data["intel"])
                obj.wisdom       = int(char_data["wisdom"])
                obj.charisma     = int(char_data["char"])
                obj.lore         = char_data.get("lore", "")
                obj.notes        = char_data.get("notes", "")
                obj.is_set       = True
                views.char_list.append(obj)
 
                index = len(views.char_list) - 1
                new_char_btn = self.sidebar._make_char_btn(obj.name)
                new_char_btn.clicked.connect(lambda _, i=index: self.sidebar.set_display(i))
                new_char_btn.customContextMenuRequested.connect(
                    lambda pos, i=index, btn=new_char_btn: self.sidebar.open_context_menu(pos, i, btn)
                )
                views.button_list.append(new_char_btn)
                insert_index = character_layout.count() - 1
                character_layout.insertWidget(insert_index, new_char_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
 
            # Restore active character
            idx = s.get("current_char_index", -1)
            if 0 <= idx < len(views.char_list):
                self.sidebar.set_display(idx)

            # Restore campaign name
            if "campaign_name" in s and s["campaign_name"]:
                self._update_title(s["campaign_name"])

            # Restore Colors
            if "body_color" in s:
                color = QColor(s["body_color"])
                d.set_body_color(color)
                self.dice.apply_accent(color)
                self.characterSheet.apply_accent(color)
                self.multipliers.apply_accent(color)
                self.sidebar.apply_accent(color) 
 
    
    
 
# init the app
app = QApplication(sys.argv)
 
# init mainwindow in the app and make maximized size
window = MainWindow()
window.showMaximized()

# launch app
app.exec()
