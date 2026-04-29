
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QFrame, QListWidget, QTextEdit, QComboBox, QWidget,QScrollArea, QSplitter, QHBoxLayout
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
        self.setStyleSheet(f"""
            SidebarView {{
                border: 4px solid {QColor(75, 20, 20)};
                border-radius: 4px;
            }}
        """)

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
    
    def apply_accent(self, color: QColor):
        self.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {color.name()};
                border-radius: 2px;
            }}
        """)


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
    # TO DO
        # Genuinely don't know what the heck is happening in this box so someone add pls
class MultiplierView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.setStyleSheet(f"""
            MultiplierView {{
                border: 2px solid #4B1414;
                border-radius: 4px;
            }}
        """)

        multiplier_layout = QVBoxLayout(self)
        
        title = QLabel("Multipliers")
        title.setFont(QFont("Inter", 24))

        multiplier_layout.addWidget(title)
        
        multi_container = QWidget()
        multi_view = QHBoxLayout(multi_container)

        # Demo Mods
        mods = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        mod_container = QWidget()
        mod_layout = QVBoxLayout(mod_container)

        for mod in mods:
            mod_layout.addWidget(QLabel(mod))
        
        add_container = QWidget()
        add_layout = QVBoxLayout(add_container)
        list = ["str", "dex", "con", "int", "wis", "char"]
        for i in list:
            add_layout.addWidget(QLabel(f"+{die.print_mod(i)}"))
        
        result_container = QWidget()
        result_layout = QVBoxLayout(result_container)
        self.result = 0
        self.result_labels = []  # save references
        for i in range(6):
            label = QLabel("0")
            self.result_labels.append(label)
            result_layout.addWidget(label)

        multi_view.addWidget(mod_container)
        multi_view.addWidget(add_container)
        multi_view.addWidget(result_container)

        multiplier_layout.addWidget(multi_container)

    def on_roll_completed(self, total: int):
        for label in self.result_labels:
            label.setText(str(total))

    def apply_accent(self, color: QColor):
        self.setStyleSheet(f"""
            MultiplierView {{
                border: 2px solid {color.name()};
                border-radius: 4px;
            }}
        """)
