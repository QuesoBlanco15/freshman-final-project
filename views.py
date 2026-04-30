
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QFrame, QListWidget, QTextEdit, QComboBox, QWidget,QScrollArea, QSplitter, QGridLayout
from diceClass import *
from widgets import *

# Sidebar View
    # TO DO
        # Add Settings
        # Add Characters
        # Add an Add Characters
    #added by Andre:
        # a character selection/creation/deletion that will be inside of the sidebar
        # A widget that adds a new Character to the bar if clicked
roll = 0     
die = Dice()
class SidebarView(QWidget):
    def __init__(self, on_open_settings=None, parent=None):
        super().__init__(parent)

        sidebar_layout = QVBoxLayout(self)
        scroll = QScrollArea() 
        scroll.setWidgetResizable(True) 
        character = QWidget() 
        character_layout = QVBoxLayout(character) 
        scroll.setWidget(character)

        
        self.settings = QPushButton()
        self.settings.setIcon(QIcon("icons/setting-lines.png"))
        self.settings.setIconSize(QSize(25, 25))
        self.settings.clicked.connect(self.show_settings)
        self._on_open_settings = on_open_settings
        

        add_char_btn = QPushButton("add")
        add_char_btn.setFixedWidth(50)
        add_char_btn.clicked.connect(lambda:self.add_new_character(character_layout))

        sidebar_layout.addWidget(scroll)
        sidebar_layout.addLayout(character_layout)
        sidebar_layout.addWidget(self.settings)
        character_layout.addWidget(add_char_btn)
        character_layout.addStretch()

    def add_new_character(self,character_layout):
        count = 0
        for i in range(character_layout.count()):
            item = character_layout.itemAt(i)
            if item.widget() is not None:
                count+=1
        char_name = str(count)
        new_char = QPushButton(char_name)
        new_char.setFixedWidth(50)
        character_layout.insertWidget(count-1,new_char)

    def show_settings(self, checked):
        self.w = SettingsView()
        self.w.show()
        if self._on_open_settings:
            self._on_open_settings(self.w)

# Character Sheet View
    # TO DO
        # Add ability to change with change of character
        # Add Import Sheet (?) 
        # Lokey don't know what else
class CharacterSheetView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.setStyleSheet(f"""
            CharacterSheetView {{
                border: 2px solid #4B1414;
                border-radius: 4px;
            }}
        """)

        content_layout = QVBoxLayout(self)
        content_layout.addWidget(QLabel("Main Content"))
        content_layout.addWidget(QTextEdit())

    def apply_accent(self, color: QColor):
        self.setStyleSheet(f"""
            CharacterSheetView {{
                border: 2px solid {color.name()};
                border-radius: 4px;
            }}
        """)

# Dice View
    # TO DO
        # Add Multiple Dice (d20, d12, d10, d8, d4)
        # Add Drag to roll maybe
        # Add Awesome Animations
class DiceView(QFrame):
    roll_completed = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setStyleSheet(f"""
            DiceView {{
                border: 2px solid #4B1414;
                border-radius: 4px;
            }}
        """)

    
        self.dice = DiceWidget(self)

        self.dice_select = QComboBox(self)
        self.dice_select.addItems(["d4", "d6", "d8", "d10", "d12", "d20"])
        self.dice_select.setCurrentText("d20")
        self.dice_select.currentTextChanged.connect(
            lambda text: self.dice.set_dice(int(text[1:]))
        )
        self.dice.roll_completed.connect(self.roll_completed)

        panel_layout = QVBoxLayout(self)
        panel_layout.addWidget(self.dice)
        panel_layout.addWidget(self.dice_select)

    def diceroll(self):
        global die
        die = Dice(self.die_type)
        global roll
        roll = str(die.roll_dice("str"))
        self.button.setText(roll)

    def apply_accent(self, color: QColor):
        self.setStyleSheet(f"""
            DiceView {{
                border: 2px solid {color.name()};
                border-radius: 4px;
            }}
        """)

        

# Multiplier View
class MultiplierView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self._apply_style("#4B1414")

        outer = QVBoxLayout(self)

        title = QLabel("Modifiers")
        title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(title)

        # Header row
        grid = QGridLayout()
        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)

        for col, text in enumerate(["Stat", "Mod", "Roll"]):
            lbl = QLabel(text)
            lbl.setFont(QFont("Inter", 10, QFont.Weight.Bold))
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #aaa; border-bottom: 1px solid #4B1414;")
            grid.addWidget(lbl, 0, col)

        stats = [
            ("Strength",     "str"),
            ("Dexterity",    "dex"),
            ("Constitution", "con"),
            ("Intelligence", "int"),
            ("Wisdom",       "wis"),
            ("Charisma",     "char"),
        ]

        self.result_labels = []

        for row, (label_text, key) in enumerate(stats, start=1):
            bg = "background: rgba(255,255,255,0.03);" if row % 2 == 0 else ""

            name_lbl = QLabel(label_text)
            name_lbl.setStyleSheet(bg)

            mod_val = die.print_mod(key)
            mod_sign = "+" if mod_val >= 0 else ""
            mod_lbl = QLabel(f"{mod_sign}{mod_val}")
            mod_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mod_lbl.setStyleSheet(f"color: #6dbf6d; font-weight: bold; {bg}")

            result_lbl = QLabel("—")
            result_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            result_lbl.setFont(QFont("Inter", 12, QFont.Weight.Bold))
            result_lbl.setStyleSheet(f"color: #e0c080; {bg}")
            self.result_labels.append(result_lbl)

            grid.addWidget(name_lbl,   row, 0)
            grid.addWidget(mod_lbl,    row, 1)
            grid.addWidget(result_lbl, row, 2)

        outer.addLayout(grid)
        outer.addStretch()

    def on_roll_completed(self, total: int):
        for label in self.result_labels:
            label.setText(str(total))

    def _apply_style(self, color):
        self.setStyleSheet(f"""
            MultiplierView {{
                border: 2px solid {color};
                border-radius: 4px;
            }}
        """)

    def apply_accent(self, color: QColor):
        self._apply_style(color.name())