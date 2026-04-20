import sys
import math
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTabWidget
from PyQt6.QtCore import Qt, QPointF, QTimer
from PyQt6.QtGui import QPainter, QPolygonF, QColor, QBrush, QPen, QFont
from diceClass import *

class DiceWidget(QWidget):
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

        # Timer for annimation (sits around 60fps i think?)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

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
                self.result = die.roll_dice()

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

        body_color = QColor(75, 20, 20) if not self.dragging else QColor(100, 30, 30)
        painter.setBrush(QBrush(body_color))
        edge_color = QColor(210, 100, 60)
        painter.setPen(QPen(edge_color, 1.8))
        painter.drawPolygon(poly)

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
            painter.setPen(QPen(QColor(180, 70, 50, 140), 1.0))
            painter.drawPolygon(tri_poly)

        painter.rotate(-self.angle) # keep the result upright

        if self.result is not None:
            num_color = QColor(255, 200, 170)
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
                painter.setPen(QColor(200, 140, 100, 160))
                fm = painter.fontMetrics()
                painter.drawText(int(-fm.horizontalAdvance("?") / 2), int(fm.height() / 3), "?")

        else:
            font = QFont("Inter", int(r * 0.2))
            painter.setFont(font)
            painter.setPen(QColor(180, 110, 80, 180))
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

class SettingsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
                            SettingsView {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 #0d0d0d, stop: 1 #1c1c1c
        );
        color: white;
    }
                           """)
        
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(False)

        for settings in ["General", "Campaign", "Customization", "About"]:
            self.tabs.addTab(SettingsWidget(), settings)

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
                            SettingsWidget {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 #ff6b6b, stop: 1 #feca5715
        );
        color: white;
    }
                           """)

        self.label = QLabel("General")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)