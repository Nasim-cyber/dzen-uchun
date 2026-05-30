"""
COMFORTGAMECLUB - Client UI
Chiroyli gaming tema, o'yinlar menyusi va bloklash oynasi
"""

import sys
import os
import subprocess
import threading
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QScrollArea, QGridLayout,
    QSizePolicy, QMessageBox, QInputDialog, QStackedWidget
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QRect, QSize
from PyQt5.QtGui import QColor, QFont, QPalette, QLinearGradient, QBrush, QPainter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from games_data import GAMES
from blocker import SystemBlocker
from client_network import ClientNetwork


# ===== RANGLAR =====
BG_DARK      = "#050510"
BG_CARD      = "#0d0d20"
BG_HEADER    = "#08081a"
ACCENT_CYAN  = "#00e5ff"
ACCENT_BLUE  = "#1a6fff"
ACCENT_PINK  = "#ff2d78"
ACCENT_GREEN = "#00ff88"
ACCENT_ORANGE= "#ff8c00"
TEXT_WHITE   = "#ffffff"
TEXT_GRAY    = "#8888aa"
BORDER_COLOR = "#1a1a3a"

STYLE_BASE = f"""
QWidget {{
    background-color: {BG_DARK};
    color: {TEXT_WHITE};
    font-family: 'Segoe UI', Arial;
}}
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{
    background: {BG_CARD};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {ACCENT_BLUE}88;
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
"""



def btn_style(color, size=13):
    return f"""
    QPushButton {{
        background-color: {color}22;
        color: {color};
        border: 1px solid {color}55;
        border-radius: 10px;
        padding: 10px 18px;
        font-weight: bold;
        font-size: {size}px;
        text-align: left;
    }}
    QPushButton:hover {{
        background-color: {color}44;
        border: 1px solid {color};
    }}
    QPushButton:pressed {{
        background-color: {color}66;
    }}
    """


class BlockScreen(QWidget):
    """Bloklash ekrani - butun ekranni qoplaydi"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setWindowState(Qt.WindowFullScreen)
        self._build()

    def _build(self):
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #050510,
                    stop:0.5 #0a0520,
                    stop:1 #050510
                );
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # Lock icon
        lock_lbl = QLabel("🔒")
        lock_lbl.setFont(QFont("Segoe UI", 80))
        lock_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lock_lbl)

        # Club nomi
        club_lbl = QLabel("COMFORTGAMECLUB")
        club_lbl.setFont(QFont("Segoe UI", 36, QFont.Bold))
        club_lbl.setAlignment(Qt.AlignCenter)
        club_lbl.setStyleSheet(f"color: {ACCENT_CYAN}; letter-spacing: 6px;")
        layout.addWidget(club_lbl)

        # Xabar
        self.msg_lbl = QLabel("SESSIYA BLOKLANGAN")
        self.msg_lbl.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.msg_lbl.setAlignment(Qt.AlignCenter)
        self.msg_lbl.setStyleSheet(f"color: {ACCENT_PINK};")
        layout.addWidget(self.msg_lbl)

        # Izoh
        info_lbl = QLabel("Iltimos, administratorga murojaat qiling")
        info_lbl.setFont(QFont("Segoe UI", 14))
        info_lbl.setAlignment(Qt.AlignCenter)
        info_lbl.setStyleSheet(f"color: {TEXT_GRAY};")
        layout.addWidget(info_lbl)

        # Vaqt
        self.time_lbl = QLabel("")
        self.time_lbl.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.time_lbl.setAlignment(Qt.AlignCenter)
        self.time_lbl.setStyleSheet(f"color: {ACCENT_ORANGE};")
        layout.addWidget(self.time_lbl)

    def set_message(self, text):
        self.msg_lbl.setText(text)

    def set_time(self, minutes):
        if minutes > 0:
            self.time_lbl.setText(f"⏳ Vaqt tugashiga: {minutes} daqiqa")
        else:
            self.time_lbl.setText("")

    def keyPressEvent(self, event):
        event.ignore()  # Hamma tugmalarni e'tiborsiz qoldirish

    def closeEvent(self, event):
        event.ignore()  # Yopishga yo'l qo'ymaslik



class GameButton(QPushButton):
    """O'yin tugmasi"""
    def __init__(self, game: dict, color: str, parent=None):
        super().__init__(parent)
        self.game = game
        self.color = color
        icon = game.get("icon", "🎮")
        name = game.get("name", "")
        self.setText(f"  {icon}  {name}")
        self.setFixedHeight(52)
        self.setStyleSheet(btn_style(color, 13))
        self.setCursor(Qt.PointingHandCursor)
        self.clicked.connect(self._launch)

    def _launch(self):
        exe = self.game.get("exe", "")
        if exe:
            try:
                subprocess.Popen(exe, shell=True)
            except Exception as e:
                QMessageBox.warning(self, "Xato", f"O'yin ishga tushmadi:\n{e}")


class CategoryWidget(QFrame):
    """Bitta kategoriya bloki"""
    def __init__(self, name: str, data: dict, parent=None):
        super().__init__(parent)
        self.color = data["color"]
        self._build(name, data)

    def _build(self, name: str, data: dict):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_CARD};
                border: 1px solid {self.color}33;
                border-left: 3px solid {self.color};
                border-radius: 12px;
                margin: 4px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        # Kategoriya sarlavhasi
        title = QLabel(name)
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet(f"color: {self.color}; background: transparent; border: none;")
        layout.addWidget(title)

        # O'yinlar grid
        grid = QGridLayout()
        grid.setSpacing(8)
        games = data["games"]
        cols = 2
        for i, game in enumerate(games):
            btn = GameButton(game, self.color)
            grid.addWidget(btn, i // cols, i % cols)
        layout.addLayout(grid)



class ClientWindow(QMainWindow):
    # Signallar (thread-safe UI yangilash)
    sig_block   = pyqtSignal(int)
    sig_unblock = pyqtSignal()
    sig_message = pyqtSignal(str)
    sig_shutdown= pyqtSignal()
    sig_restart = pyqtSignal()
    sig_set_time= pyqtSignal(int)
    sig_connect = pyqtSignal()
    sig_disconnect = pyqtSignal()

    def __init__(self, server_ip: str):
        super().__init__()
        self.server_ip = server_ip
        self.blocker = SystemBlocker()
        self.block_screen = None
        self.time_left = 0
        self._timer_running = False

        self.setWindowTitle("COMFORTGAMECLUB")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.showFullScreen()
        self.setStyleSheet(STYLE_BASE)

        self._build_ui()
        self._connect_signals()
        self._start_network()

        # Vaqt hisoblagich
        self._time_timer = QTimer()
        self._time_timer.timeout.connect(self._tick_time)
        self._time_timer.start(60000)  # har daqiqada

    # ─── UI QURILISHI ──────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._build_header())

        # Asosiy kontent
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(20, 16, 20, 20)
        self.content_layout.setSpacing(14)

        for name, data in GAMES.items():
            cat = CategoryWidget(name, data)
            self.content_layout.addWidget(cat)

        self.scroll.setWidget(content_widget)
        layout.addWidget(self.scroll)

        layout.addWidget(self._build_footer())

    def _build_header(self):
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #050515,
                    stop:0.4 #0a1040,
                    stop:0.6 #0a1040,
                    stop:1 #050515
                );
                border-bottom: 2px solid {ACCENT_BLUE}88;
            }}
        """)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)

        # Logo
        icon_lbl = QLabel("🎮")
        icon_lbl.setFont(QFont("Segoe UI", 32))
        layout.addWidget(icon_lbl)

        name_col = QVBoxLayout()
        title = QLabel("COMFORTGAMECLUB")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet(f"color: {ACCENT_CYAN}; letter-spacing: 4px;")
        slogan = QLabel("PREMIUM GAMING EXPERIENCE")
        slogan.setFont(QFont("Segoe UI", 9))
        slogan.setStyleSheet(f"color: {TEXT_GRAY}; letter-spacing: 3px;")
        name_col.addWidget(title)
        name_col.addWidget(slogan)
        layout.addLayout(name_col)
        layout.addStretch()

        # Status va Vaqt
        right_col = QVBoxLayout()
        right_col.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.status_lbl = QLabel("● Server bilan bog'lanmoqda...")
        self.status_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.status_lbl.setStyleSheet(f"color: {ACCENT_ORANGE};")
        self.status_lbl.setAlignment(Qt.AlignRight)

        self.time_lbl = QLabel("")
        self.time_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.time_lbl.setStyleSheet(f"color: {ACCENT_GREEN};")
        self.time_lbl.setAlignment(Qt.AlignRight)

        right_col.addWidget(self.status_lbl)
        right_col.addWidget(self.time_lbl)
        layout.addLayout(right_col)
        return header

    def _build_footer(self):
        footer = QFrame()
        footer.setFixedHeight(36)
        footer.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_HEADER};
                border-top: 1px solid {BORDER_COLOR};
            }}
        """)
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(20, 0, 20, 0)
        lbl = QLabel("© COMFORTGAMECLUB  |  Barcha huquqlar himoyalangan")
        lbl.setStyleSheet(f"color: {TEXT_GRAY}; font-size: 10px;")
        layout.addWidget(lbl)
        layout.addStretch()
        import socket as _socket
        try:
            pc = _socket.gethostname()
        except:
            pc = "PC"
        pc_lbl = QLabel(f"🖥️  {pc}")
        pc_lbl.setStyleSheet(f"color: {TEXT_GRAY}; font-size: 10px;")
        layout.addWidget(pc_lbl)
        return footer


    # ─── SIGNALLAR ─────────────────────────────────────────

    def _connect_signals(self):
        self.sig_block.connect(self._do_block)
        self.sig_unblock.connect(self._do_unblock)
        self.sig_message.connect(self._do_message)
        self.sig_shutdown.connect(self._do_shutdown)
        self.sig_restart.connect(self._do_restart)
        self.sig_set_time.connect(self._do_set_time)
        self.sig_connect.connect(self._do_connect)
        self.sig_disconnect.connect(self._do_disconnect)

    # ─── TARMOQ ────────────────────────────────────────────

    def _start_network(self):
        callbacks = {
            "on_block":      lambda m: self.sig_block.emit(m),
            "on_unblock":    lambda:   self.sig_unblock.emit(),
            "on_shutdown":   lambda:   self.sig_shutdown.emit(),
            "on_restart":    lambda:   self.sig_restart.emit(),
            "on_message":    lambda t: self.sig_message.emit(t),
            "on_set_time":   lambda m: self.sig_set_time.emit(m),
            "on_connect":    lambda:   self.sig_connect.emit(),
            "on_disconnect": lambda:   self.sig_disconnect.emit(),
        }
        self.network = ClientNetwork(callbacks)
        self.network.start(self.server_ip)

    # ─── EVENT HANDLERLARI ─────────────────────────────────

    def _do_block(self, minutes: int):
        self.time_left = minutes
        self.blocker.block()
        if not self.block_screen:
            self.block_screen = BlockScreen()
        self.block_screen.set_time(minutes)
        self.block_screen.show()
        self.block_screen.activateWindow()
        self.block_screen.raise_()
        self._update_time_label()

    def _do_unblock(self):
        self.time_left = 0
        self.blocker.unblock()
        if self.block_screen:
            self.block_screen.hide()
        self.time_lbl.setText("")
        self._update_time_label()

    def _do_message(self, text: str):
        msg = QMessageBox(self)
        msg.setWindowTitle("Admin xabari")
        msg.setText(f"💬  {text}")
        msg.setStyleSheet(f"QWidget {{ background: #12122a; color: white; }}")
        msg.exec_()

    def _do_shutdown(self):
        import subprocess
        subprocess.Popen("shutdown /s /t 10 /c \"Admin tomonidan o'chirilmoqda...\"", shell=True)

    def _do_restart(self):
        import subprocess
        subprocess.Popen("shutdown /r /t 10 /c \"Admin tomonidan qayta yoqilmoqda...\"", shell=True)

    def _do_set_time(self, minutes: int):
        self.time_left = minutes
        self._update_time_label()
        if self.block_screen:
            self.block_screen.set_time(minutes)

    def _do_connect(self):
        self.status_lbl.setText("● Admin bilan ulangan")
        self.status_lbl.setStyleSheet(f"color: {ACCENT_GREEN};")

    def _do_disconnect(self):
        self.status_lbl.setText("● Server bilan bog'lanmoqda...")
        self.status_lbl.setStyleSheet(f"color: {ACCENT_ORANGE};")

    def _tick_time(self):
        if self.time_left > 0:
            self.time_left -= 1
            self._update_time_label()
            if self.block_screen:
                self.block_screen.set_time(self.time_left)
            if self.time_left == 0:
                self._do_unblock()

    def _update_time_label(self):
        if self.time_left > 0:
            self.time_lbl.setText(f"⏱️  Qolgan vaqt: {self.time_left} daq")
        else:
            self.time_lbl.setText("")

    # ─── TIZIM TUGMALARI BLOKLASH ──────────────────────────

    def keyPressEvent(self, event):
        if self.blocker.is_blocked:
            event.ignore()
            return
        # Alt+F4 ni bloklash
        if event.key() == Qt.Key_F4 and event.modifiers() == Qt.AltModifier:
            event.ignore()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        if self.blocker.is_blocked:
            event.ignore()
            return
        self.network.stop()
        self.blocker.unblock()
        event.accept()


# ─── MAIN ──────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default="127.0.0.1",
                        help="Admin server IP manzili")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BG_DARK))
    palette.setColor(QPalette.WindowText, QColor(TEXT_WHITE))
    palette.setColor(QPalette.Base, QColor(BG_CARD))
    palette.setColor(QPalette.Text, QColor(TEXT_WHITE))
    palette.setColor(QPalette.Button, QColor(BG_CARD))
    palette.setColor(QPalette.ButtonText, QColor(TEXT_WHITE))
    palette.setColor(QPalette.Highlight, QColor(ACCENT_BLUE))
    app.setPalette(palette)

    win = ClientWindow(args.server)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
