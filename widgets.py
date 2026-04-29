import sys
import math
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTabWidget, QFrame, QHBoxLayout, QPushButton, QColorDialog, QCheckBox, QComboBox, QScrollArea, QLineEdit, QStyle
from PyQt6.QtCore import Qt, QPointF, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QPolygonF, QColor, QBrush, QPen, QFont
from diceClass import *

#############################################
# Dice Widget
# The Widget resposnible for rolling dice  
# Written by Cayson
#############################################
class DiceWidget(QWidget):
    roll_completed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.OpenHandCursor)

        # dice states
        self.dice_type = 20
        self.dice_pos = QPointF(150,150)
        self.angle = 0.0
        self.spin_dir = 1
        self.spin_speed = 0.0
        self.rolling = False
        self.result: int | None = None
        self.scale = 1.0
        self.dragging = False
        self.drag_offset = QPointF()
        self.last_cursor = QPointF()
        self.velocity = QPointF()
        self.travel_vel = QPointF()
        self.body_color = QColor(75, 20, 20)
        self.edge_color = QColor(210, 100, 60)
        self.num_color = QColor(255, 200, 170)
        self.show_triangle = True

        # Timer for annimation (sits around 60fps i think?)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

    def set_body_color(self, value):
        self.body_color = value
        self.update()

    def set_edge_color(self, value):
        self.edge_color = value
        self.update()

    def set_num_color(self, value):
        self.num_color = value
        self.update()

    def set_show_triangle(self, value):
        self.show_triangle = value
        self.update()

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        pos = event.position()
        if self._hit_test(pos):
            self.dragging = True
            self.rolling = False
            self.result = None
            self.spin_speed = 0.0
            self.drag_offset = pos - self.dice_pos
            self.last_cursor = pos
            self.velocity = QPointF(0, 0)
            self.scale = 1.10 # Effect of picking up the dice
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        
    def mouseMoveEvent(self, event):
        if not self.dragging:
            return
        pos = event.position()

        raw_vel = pos - self.last_cursor
        self.velocity = self.velocity * 0.5 + raw_vel * 0.5 # edit ints for smoother velo
        self.last_cursor = pos
        self.dice_pos = pos - self.drag_offset
        self._clamp_dice_pos()
        self.update()

    def mouseReleaseEvent(self, event):
        if not self.dragging:
            return
        self.dragging = False
        self.scale = 1.0
        self.setCursor(Qt.CursorShape.OpenHandCursor)

        speed = math.hypot(self.velocity.x(), self.velocity.y())
        if speed < 1.5:
            speed = 6.0
            self.travel_vel = QPointF(0, 0)
        else:
            scale = min(speed * 0.9, 28.0) / max(speed, 0.001)
            self.travel_vel = QPointF(
                self.velocity.x() * scale * 0.9,
                self.velocity.y() * scale * 0.9,
            )

        self.spin_speed = min(speed * 0.9, 28.0)
        self.spin_dir = 1 if self.velocity.x() >= 0 else -1 #Error implement
        self.rolling = True
        self.result = None

    def _tick(self):
        if self.rolling:
            self.angle += self.spin_dir * self.spin_speed
            self.spin_speed *= 0.95

            if (abs(self.travel_vel.x()) > 0.05 or abs(self.travel_vel.y()) > 0.05):
                self.dice_pos += self.travel_vel
                self.travel_vel *= 0.95
                self._clamp_dice_pos()

            if self.spin_speed < 0.5:
                die = Dice(self.dice_type)
                self.rolling = False
                self.result = die.roll_dice("str")
                self.roll_completed.emit(int(self.result))

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self._draw_die(painter)

        painter.end()
    
    def _draw_die(self, painter: QPainter):
        cx, cy = self.dice_pos.x(), self.dice_pos.y()
        r = 72 * self.scale

        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.angle)

        if self.dice_type == 20:
            sides = 6
        elif self.dice_type == 12:
            sides = 5
        elif self.dice_type == 10:
            sides = 4
        elif self.dice_type == 8:
            sides = 3
        elif self.dice_type == 6:
            sides = 4
        elif self.dice_type == 4:
            sides = 3
        points = [
            QPointF(
                r * math.cos(math.radians(i * 360 / sides - 90)),
                r * math.sin(math.radians(i * 360 / sides - 90)),
            )
            for i in range(sides)
        ]
        poly = QPolygonF(points)

        shadow_color = QColor(20, 0, 0, 50)
        painter.setBrush(QBrush(shadow_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.translate(4, 6)
        painter.drawPolygon(poly)
        painter.translate(-4, -6)

        body_color = self.body_color 
        painter.setBrush(QBrush(body_color))
        edge_color = self.edge_color
        painter.setPen(QPen(edge_color, 1.8))
        painter.drawPolygon(poly)

        if self.show_triangle == True:
            if (self.dice_type != 4) or (self.dice_type != 6):
                tri_r = r * .65
                tri_pts = [
                    QPointF(
                        tri_r * math.cos(math.radians(i * 120 - 90)),
                        tri_r * math.sin(math.radians(i * 120 - 90)),
                    )
                    for i in range(3)
                ]
                tri_poly = QPolygonF(tri_pts)
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.setPen(QPen(edge_color, 1.0))
                painter.drawPolygon(tri_poly)

        painter.rotate(-self.angle) # keep the result upright

        if self.result is not None:
            num_color = self.num_color
            font = QFont("Inter", int(r * 0.4), QFont.Weight.Bold)
            painter.setFont(font)
            painter.setPen(num_color)

            text = str(self.result)
            fm = painter.fontMetrics()
            tw = fm.horizontalAdvance(text)
            th = fm.height()
            painter.drawText(int(-tw /2), int(th /3), text)

        elif self.rolling:
            if self.spin_speed > 4:
                font = QFont("Inter", int(r * 0.4), QFont.Weight.Bold)
                painter.setFont(font)
                painter.setPen(self.num_color)
                fm = painter.fontMetrics()
                painter.drawText(int(-fm.horizontalAdvance("?") / 2), int(fm.height() / 3), "?")

        else:
            font = QFont("Inter", int(r * 0.2))
            painter.setFont(font)
            painter.setPen(self.num_color)
            message = "Drag to Throw"
            fm = painter.fontMetrics()
            painter.drawText(int(-fm.horizontalAdvance(message) / 2), int(fm.height() / 3), message)

        painter.restore()

    def _hit_test(self, pos: QPointF) -> bool:
        dx = pos.x() - self.dice_pos.x()
        dy = pos.y() - self.dice_pos.y()
        return math.hypot(dx, dy) <= 72 * self.scale
    
    def _clamp_dice_pos(self):
        margin = 80
        self.dice_pos.setX(max(margin, min(self.width() - margin, self.dice_pos.x())))
        self.dice_pos.setY(max(margin, min(self.height() - margin, self.dice_pos.y())))

    def set_dice(self, sides: int):
        self.dice_type = sides
        self.result = None
        self.update()

    def resizeEvent(self, event):
        self.dice_pos = QPointF(self.width() / 2, self.height() / 2)
        super().resizeEvent(event)

#############################################
# Settings Widget
# The Widget for the settings pop up.
# Written by Cayson
#############################################

# Helper functions

def section_label(text: str) -> QLabel:
    label = QLabel(text.upper())
    label.setFont(QFont("Inter", 9, QFont.Weight.Bold))
    label.setStyleSheet("color: #888; letter-spacing: 1.5px; margin-top: 8px;")
    return label

def divider() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setStyleSheet("color: #2a2a2a;")
    return line

class RowWidget(QWidget):
    def __init__(self, title: str, desc: str = "", control: QWidget = None, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)

        text_col = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setFont(QFont("Inter", 11, QFont.Weight.Medium))
        text_col.addWidget(title_label)

        if desc:
            desc_label = QLabel(desc)
            desc_label.setFont(QFont("Inter", 9))  # FIX 2: was setFont("Inter", 9)
            desc_label.setStyleSheet("color: #888;")
            text_col.addWidget(desc_label)

        layout.addLayout(text_col)
        layout.addStretch()

        if control:
            layout.addWidget(control)

class ColorButton(QPushButton):
    color_changed = pyqtSignal(QColor)

    def __init__(self, init_color: QColor, parent=None):
        super().__init__(parent)
        self.setFixedSize(32, 32)
        self.setColor(init_color)
        self.clicked.connect(self._pick)

    def setColor(self, color: QColor):
        self._color = color
        self.setStyleSheet(
            f"background-color: {color.name()};"
            "border-radius: 6px;"
            "border: 1.5px solid #555" 
        )
    
    def color(self) -> QColor:
        return self._color
    
    def _pick(self):
        dialog = QColorDialog(self._color, self)
        dialog.setOption(QColorDialog.ColorDialogOption.DontUseNativeDialog, True)
        dialog.setStyleSheet("* { background-color: none; color: none; }")
        for child in dialog.findChildren(QWidget):
            child.setStyleSheet("")
        if dialog.exec():
            picked = dialog.selectedColor()
            if picked.isValid():
                self.setColor(picked)
                self.color_changed.emit(picked)

class ToggleSwitch(QCheckBox):
    def __init__(self, checked: bool = False, parent=None):
        super().__init__(parent)
        self.setChecked(checked)
        self.stateChanged.connect(lambda _: self._update_style())
        self._update_style()  # FIX 3: apply style on init
    
    def _update_style(self):
        if self.isChecked():
            self.setStyleSheet("""
                QCheckBox::indicator { width: 40px; height: 22px; border-radius: 11px;
                    background: #378ADD; border: none; }
                QCheckBox::indicator:checked { image: none; }
                QCheckBox { spacing: 0; }
            """)
        else:
            self.setStyleSheet("""
                QCheckBox::indicator { width: 40px; height: 22px; border-radius: 11px;
                    background: #444; border: none; }
                QCheckBox { spacing: 0; }
            """)
    
def styled_combo(options: list[str], current: str = "") -> QComboBox:
    cb = QComboBox()
    cb.addItems(options)
    if current:
        cb.setCurrentText(current)
    cb.setStyleSheet("""
        QComboBox {
            background: #1e1e1e; color: #e8e8e8;
            border: 0.5px solid #444; border-radius: 6px;
            padding: 4px 10px; font-size: 12px; min-width: 100px;
        }
        QComboBox::drop-down { border: none; }
        QComboBox QAbstractItemView { background: #1e1e1e; color: #e8e8e8; selection-background-color: #2a2a2a; }
    """)
    return cb
    
class SectionCard(QWidget):
    def __init__(self, rows: list[QWidget], parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            SectionCard {
                background: #1a1a1a;
                border: 0.5px solid #2e2e2e;
                border-radius: 12px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        for i, row in enumerate(rows):
            layout.addWidget(row)
            if i < len(rows) - 1:
                layout.addWidget(divider())

class NavWidget(QWidget):
    section_clicked = pyqtSignal(str)

    SECTIONS = ["General", "Customization", "About"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            FloatingNav {
                background: #1a1a1a;
                border: 0.5px solid #2e2e2e;
                border-radius: 10px;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        self._buttons: dict[str, QPushButton] = {}
        for name in self.SECTIONS:
            btn = QPushButton(name)
            btn.setFont(QFont("Inter", 10))
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, n=name: self._on_click(n))
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent; color: #888;
                    border: none; border-radius: 6px;
                    padding: 5px 14px;
                }
                QPushButton:checked {
                    background: #1d3a5c; color: #5aabff;
                }
                QPushButton:hover:!checked { background: #222; color: #ccc; }
            """)
            self._buttons[name] = btn
            layout.addWidget(btn)

        self._buttons["General"].setChecked(True)

    def _on_click(self, name: str):
        for n, b in self._buttons.items():
            b.setChecked(n == name)
        self.section_clicked.emit(name)

    def set_active(self, name: str):
        for n, b in self._buttons.items():
            b.setChecked(n == name)

class SettingsView(QWidget):
    dice_body_color_changed = pyqtSignal(QColor)
    dice_edge_color_changed = pyqtSignal(QColor)
    dice_number_color_changed = pyqtSignal(QColor)
    inner_triangle_toggled = pyqtSignal(bool)
    default_die_changed = pyqtSignal(int)
    animation_speed_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(480)
        self.resize(560, 680)
        self.setWindowTitle("Settings")
        self.setStyleSheet("""
            SettingsView {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0d0d0d, stop:1 #1c1c1c);
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(12)

        self.nav = NavWidget()
        self.nav.setFixedHeight(42)
        root.addWidget(self.nav)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.scroll.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical { width: 6px; background: transparent; }
            QScrollBar::handle:vertical { background: #333; border-radius: 3px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        self._content_layout = QVBoxLayout(content)
        self._content_layout.setContentsMargins(0, 8, 0, 40)
        self._content_layout.setSpacing(20)

        self._section_widgets: dict[str, QWidget] = {}

        self._build_general()
        self._build_customization()
        self._build_about()

        self._content_layout.addStretch()
        self.scroll.setWidget(content)
        root.addWidget(self.scroll)

        self.nav.section_clicked.connect(self._scroll_to)

    def _add_section(self, name: str, label_widget: QLabel, card: SectionCard):
        wrapper = QWidget()
        wrapper.setStyleSheet("background: transparent;")
        vl = QVBoxLayout(wrapper)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(6)
        vl.addWidget(label_widget)
        vl.addWidget(card)
        self._content_layout.addWidget(wrapper)
        self._section_widgets[name] = wrapper

    def _build_general(self):
        self.campaign_input = QLineEdit()
        self.campaign_input.setPlaceholderText("My Campaign")
        self.campaign_input.setFixedWidth(180)
        self.campaign_input.setStyleSheet("""
            QLineEdit {
                background: #1e1e1e; color: #e8e8e8;
                border: 0.5px solid #444; border-radius: 6px;
                padding: 4px 10px; font-size: 12px;
            }
        """)
    
        self.default_die_combo = styled_combo(["d4", "d6", "d8", "d10", "d12", "d20"], "d20")
        self.default_die_combo.currentTextChanged.connect(
            lambda t: self.default_die_changed.emit(int(t[1:]))
        )

        rows = [
            RowWidget("Campaign name", "Active campaign or session title", self.campaign_input),
            RowWidget("Default die", "Die shown on startup", self.default_die_combo),
        ]

        self._add_section("General", section_label("General"), SectionCard(rows))
    
    def _build_customization(self):
        self.THEMES = {
            "Crimson": (QColor(75, 20, 20),   QColor(210, 100, 60),  QColor(255, 200, 170)),
            "Arcane":  (QColor(30, 15, 60),   QColor(130, 80, 220),  QColor(210, 180, 255)),
            "Forest":  (QColor(15, 45, 20),   QColor(60, 160, 80),   QColor(180, 240, 190)),
            "Bone": (QColor(45, 38, 28), QColor(180, 160, 110), QColor(235, 220, 185)),
        }
        self._active_theme: str | None = "Crimson"

        theme_picker = QWidget()
        theme_picker.setStyleSheet("background: transparent;")
        tp_layout = QHBoxLayout(theme_picker)
        tp_layout.setContentsMargins(16, 14, 16, 14)
        tp_layout.setSpacing(0)

        label_col = QVBoxLayout()
        tl = QLabel("Theme")
        tl.setFont(QFont("Inter", 11, QFont.Weight.Medium))
        tl.setStyleSheet("color: #e8e8e8;")
        td = QLabel("Pick a preset colour scheme")
        td.setFont(QFont("Inter", 9))
        td.setStyleSheet("color: #888;")
        label_col.addWidget(tl)
        label_col.addWidget(td)
        tp_layout.addLayout(label_col)
        tp_layout.addStretch()

        self._theme_buttons: dict[str, QPushButton] = {}
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        for name, (body, edge, _num) in self.THEMES.items():
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setFont(QFont("Inter", 10))
            btn.setFixedHeight(30)
            btn.setStyleSheet(self._theme_btn_style(body, edge, checked=name == "Crimson"))
            btn.clicked.connect(lambda _, n=name: self._apply_theme(n))
            self._theme_buttons[name] = btn
            btn_row.addWidget(btn)
        tp_layout.addLayout(btn_row)

        self._advanced_visible = False
        adv_toggle = QPushButton("Advanced  ▸")
        adv_toggle.setFont(QFont("Inter", 10))
        adv_toggle.setStyleSheet("""
            QPushButton {
                background: transparent; color: #666;
                border: none; padding: 12px 16px;
                text-align: left;
            }
            QPushButton:hover { color: #aaa; }
        """)
        adv_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        adv_toggle.clicked.connect(lambda: self._toggle_advanced(adv_toggle))

        self._advanced_panel = QWidget()
        self._advanced_panel.setStyleSheet("background: transparent;")
        self._advanced_panel.setVisible(False)
        adv_layout = QVBoxLayout(self._advanced_panel)
        adv_layout.setContentsMargins(0, 0, 0, 0)
        adv_layout.setSpacing(0)

        adv_layout.addWidget(divider())

        self.body_color_btn = ColorButton(QColor(75, 20, 20))
        self.body_color_btn.color_changed.connect(self.dice_body_color_changed)
        self.body_color_btn.color_changed.connect(lambda _: self._clear_theme())

        self.edge_color_btn = ColorButton(QColor(210, 100, 60))
        self.edge_color_btn.color_changed.connect(self.dice_edge_color_changed)
        self.edge_color_btn.color_changed.connect(lambda _: self._clear_theme())

        self.number_color_btn = ColorButton(QColor(255, 200, 170))
        self.number_color_btn.color_changed.connect(self.dice_number_color_changed)
        self.number_color_btn.color_changed.connect(lambda _: self._clear_theme())

        self.triangle_toggle = ToggleSwitch(checked=True)
        self.triangle_toggle.stateChanged.connect(
            lambda state: self.inner_triangle_toggled.emit(state == 2)
        )

        for row in [
            RowWidget("Primary Color",  "Main fill of the die",           self.body_color_btn),
            RowWidget("Secondary Color","Outline and inner glow",          self.edge_color_btn),
            RowWidget("Text Color",     "Color of the roll result & all text", self.number_color_btn),
            RowWidget("Inner triangle",   "Show inner triangle decoration",  self.triangle_toggle),
        ]:
            adv_layout.addWidget(row)
            adv_layout.addWidget(divider())

        last = adv_layout.itemAt(adv_layout.count() - 1)
        if last and last.widget():
            last.widget().deleteLater()

        card = QWidget()
        card.setStyleSheet("""
            QWidget#customCard {
                background: #1a1a1a;
                border: 0.5px solid #2e2e2e;
                border-radius: 12px;
            }
        """)
        card.setObjectName("customCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        card_layout.addWidget(theme_picker)
        card_layout.addWidget(divider())
        card_layout.addWidget(adv_toggle)
        card_layout.addWidget(self._advanced_panel)

        wrapper = QWidget()
        wrapper.setStyleSheet("background: transparent;")
        vl = QVBoxLayout(wrapper)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(6)
        vl.addWidget(section_label("Customization"))
        vl.addWidget(card)
        self._content_layout.addWidget(wrapper)
        self._section_widgets["Customization"] = wrapper

    def _theme_btn_style(self, body: QColor, edge: QColor, checked: bool) -> str:
        border = edge.name()
        bg = body.lighter(140).name() if checked else body.darker(120).name()
        text = edge.lighter(160).name() if checked else "#777"
        outline = f"2px solid {border}" if checked else f"0.5px solid {body.lighter(160).name()}"
        return f"""
            QPushButton {{
                background: {bg}; color: {text};
                border: {outline}; border-radius: 6px;
                padding: 0 14px; font-size: 11px;
            }}
            QPushButton:hover {{ background: {body.lighter(160).name()}; color: {edge.lighter(160).name()}; }}
        """

    def _apply_theme(self, name: str):
        self._active_theme = name
        body, edge, num = self.THEMES[name]

        self.body_color_btn.setColor(body)
        self.edge_color_btn.setColor(edge)
        self.number_color_btn.setColor(num)

        self.dice_body_color_changed.emit(body)
        self.dice_edge_color_changed.emit(edge)
        self.dice_number_color_changed.emit(num)

        for n, btn in self._theme_buttons.items():
            b, e, _ = self.THEMES[n]
            btn.setStyleSheet(self._theme_btn_style(b, e, checked=(n == name)))
            btn.setChecked(n == name)

    def _clear_theme(self):
        self._active_theme = None
        for n, btn in self._theme_buttons.items():
            b, e, _ = self.THEMES[n]
            btn.setChecked(False)
            btn.setStyleSheet(self._theme_btn_style(b, e, checked=False))

    def _toggle_advanced(self, toggle_btn: QPushButton):
        self._advanced_visible = not self._advanced_visible
        self._advanced_panel.setVisible(self._advanced_visible)
        arrow = "▾" if self._advanced_visible else "▸"
        toggle_btn.setText(f"Advanced  {arrow}")

    def _build_about(self):
        wrapper = QWidget()
        wrapper.setStyleSheet("background: transparent;")
        vl = QVBoxLayout(wrapper)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(6)
        vl.addWidget(section_label("About"))

        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background: #1a1a1a;
                border: 0.5px solid #2e2e2e;
                border-radius: 12px;
            }
        """)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(16, 16, 16, 16)
        cl.setSpacing(4)

        name = QLabel("John DnD")
        name.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        name.setStyleSheet("color: #e8e8e8; border: none;")

        version = QLabel("Version 0.1.0")
        version.setFont(QFont("Inter", 10))
        version.setStyleSheet("color: #666; border: none;")

        authors = QLabel("A Group 5 project.")
        authors.setFont(QFont("Inter", 10))
        authors.setStyleSheet("color: #888; margin-top: 8px; border: none;")

        cl.addWidget(name)
        cl.addWidget(version)
        cl.addWidget(authors)

        vl.addWidget(card)
        self._content_layout.addWidget(wrapper)
        self._section_widgets["About"] = wrapper

    def _scroll_to(self, name: str):
        widget = self._section_widgets.get(name)
        if widget:
            self.scroll.ensureWidgetVisible(widget, 0, 0)