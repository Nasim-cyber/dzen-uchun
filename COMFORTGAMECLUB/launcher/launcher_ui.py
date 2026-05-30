"""
COMFORTGAMECLUB - DarkShell uslubida Gaming Launcher
PyQt5 bilan yaratilgan professional game club interfeysi
"""

import sys, os, subprocess, time, threading
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QGridLayout,
    QStackedWidget, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize, QPoint
from PyQt5.QtGui import (
    QColor, QFont, QPalette, QPainter, QLinearGradient,
    QBrush, QCursor, QIcon, QRadialGradient
)

sys.path.insert(0, os.path.dirname(__file__))
from launcher_data import LAUNCHERS, GAMES

# ═══════════════════════════════════════════════════════
#  RANGLAR
# ═══════════════════════════════════════════════════════
C_BG       = "#0b0b1a"
C_BG2      = "#0f0f22"
C_CARD     = "#13132a"
C_CARD2    = "#1c1c38"
C_BORDER   = "#2a2a4a"
C_PURPLE   = "#7b2fff"
C_PURPLE2  = "#9d4edd"
C_CYAN     = "#00e5ff"
C_PINK     = "#ff2d78"
C_GREEN    = "#00ff88"
C_ORANGE   = "#ff8c00"
C_YELLOW   = "#ffe600"
C_TEXT     = "#c8c8e8"
C_MUTED    = "#5555aa"

# ═══════════════════════════════════════════════════════
#  YORDAMCHI FUNKSIYALAR
# ═══════════════════════════════════════════════════════
def glow(widget, color="#7b2fff", radius=18):
    ef = QGraphicsDropShadowEffect()
    ef.setBlurRadius(radius)
    ef.setColor(QColor(color))
    ef.setOffset(0, 0)
    widget.setGraphicsEffect(ef)
    return ef

def make_font(size, bold=False, family="Segoe UI"):
    f = QFont(family, size)
    f.setBold(bold)
    return f

def orbitron(size, bold=True):
    f = QFont("Orbitron", size)
    f.setBold(bold)
    return f

# ═══════════════════════════════════════════════════════
#  LAUNCHER KARTA
# ═══════════════════════════════════════════════════════
class LauncherCard(QFrame):
    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data
        self.setFixedSize(90, 100)
        self.setCursor(Qt.PointingHandCursor)
        self._build()

    def _build(self):
        self.setStyleSheet(f"""
            QFrame {{
                background: {self.data['bg']};
                border: 1px solid #2a2a4a;
                border-radius: 14px;
            }}
            QFrame:hover {{
                border: 1px solid {self.data['color']};
                background: {self.data['bg']};
            }}
        """)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 10, 8, 8)
        lay.setSpacing(4)
        lay.setAlignment(Qt.AlignCenter)

        ico = QLabel(self.data["icon"])
        ico.setFont(QFont("Segoe UI Emoji", 28))
        ico.setAlignment(Qt.AlignCenter)
        lay.addWidget(ico)

        name = QLabel(self.data["name"])
        name.setFont(make_font(9, bold=True))
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet(f"color: #9999cc; background: transparent; border: none;")
        name.setWordWrap(True)
        lay.addWidget(name)

    def mousePressEvent(self, e):
        try:
            subprocess.Popen(self.data["exe"], shell=True)
        except:
            pass

    def enterEvent(self, e):
        glow(self, self.data["color"], 20)
        self.setStyleSheet(f"""
            QFrame {{
                background: {self.data['bg']};
                border: 1px solid {self.data['color']};
                border-radius: 14px;
            }}
        """)

    def leaveEvent(self, e):
        self.setGraphicsEffect(None)
        self.setStyleSheet(f"""
            QFrame {{
                background: {self.data['bg']};
                border: 1px solid #2a2a4a;
                border-radius: 14px;
            }}
        """)

# ═══════════════════════════════════════════════════════
#  O'YIN KARTA
# ═══════════════════════════════════════════════════════
class GameCard(QFrame):
    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data
        self.setFixedSize(148, 200)
        self.setCursor(Qt.PointingHandCursor)
        self._build()

    def _build(self):
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 {self.data['color']}aa, stop:1 #0d0d20);
                border: 1px solid #252540;
                border-radius: 14px;
            }}
        """)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Thumb
        thumb = QFrame()
        thumb.setFixedHeight(130)
        thumb.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 {self.data['color']}cc,
                    stop:1 #080818);
                border-top-left-radius: 14px;
                border-top-right-radius: 14px;
                border: none;
            }}
        """)
        t_lay = QVBoxLayout(thumb)
        t_lay.setAlignment(Qt.AlignCenter)

        ico = QLabel(self.data["icon"])
        ico.setFont(QFont("Segoe UI Emoji", 48))
        ico.setAlignment(Qt.AlignCenter)
        ico.setStyleSheet("background: transparent; border: none;")
        t_lay.addWidget(ico)

        # Badge
        if self.data.get("badge"):
            badge_colors = {
                "HOT": ("#ff2d78", "#330010"),
                "TOP": ("#ffe600", "#332200"),
                "NEW": ("#00ff88", "#003322"),
            }
            bc, bb = badge_colors.get(self.data["badge"], (C_CYAN, "#002233"))
            badge = QLabel(self.data["badge"])
            badge.setFont(make_font(8, bold=True))
            badge.setAlignment(Qt.AlignCenter)
            badge.setFixedWidth(40)
            badge.setStyleSheet(f"""
                color: {bc};
                background: {bb};
                border: 1px solid {bc}88;
                border-radius: 5px;
                padding: 1px 4px;
            """)
            badge.move(8, 8)
            badge.setParent(thumb)

        lay.addWidget(thumb)

        # Info
        info = QFrame()
        info.setStyleSheet(f"""
            QFrame {{
                background: rgba(10,10,25,0.95);
                border-bottom-left-radius: 14px;
                border-bottom-right-radius: 14px;
                border: none;
            }}
        """)
        i_lay = QVBoxLayout(info)
        i_lay.setContentsMargins(10, 8, 10, 10)
        i_lay.setSpacing(2)

        title = QLabel(self.data["name"])
        title.setFont(make_font(10, bold=True))
        title.setStyleSheet("color: #ddddee; background: transparent; border: none;")
        title.setWordWrap(True)

        genre = QLabel(self.data["genre"])
        genre.setFont(make_font(9))
        genre.setStyleSheet(f"color: {C_MUTED}; background: transparent; border: none;")

        i_lay.addWidget(title)
        i_lay.addWidget(genre)
        lay.addWidget(info)

    def mousePressEvent(self, e):
        try:
            subprocess.Popen(self.data["exe"], shell=True)
        except:
            pass

    def enterEvent(self, e):
        glow(self, self.data["color"], 25)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 {self.data['color']}cc, stop:1 #0d0d20);
                border: 1px solid {self.data['color']};
                border-radius: 14px;
            }}
        """)

    def leaveEvent(self, e):
        self.setGraphicsEffect(None)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 {self.data['color']}aa, stop:1 #0d0d20);
                border: 1px solid #252540;
                border-radius: 14px;
            }}
        """)

# ═══════════════════════════════════════════════════════
#  SIDEBAR TUGMA
# ═══════════════════════════════════════════════════════
class SideBtn(QLabel):
    def __init__(self, icon, tooltip="", parent=None):
        super().__init__(icon, parent)
        self.setToolTip(tooltip)
        self.setFixedSize(42, 42)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Segoe UI Emoji", 18))
        self.setCursor(Qt.PointingHandCursor)
        self._normal()

    def _normal(self):
        self.setStyleSheet(f"""
            QLabel {{
                background: rgba(255,255,255,0.04);
                border: 1px solid transparent;
                border-radius: 11px;
                color: #6666aa;
            }}
        """)

    def enterEvent(self, e):
        self.setStyleSheet(f"""
            QLabel {{
                background: rgba(123,47,255,0.2);
                border: 1px solid {C_PURPLE};
                border-radius: 11px;
                color: white;
            }}
        """)
        glow(self, C_PURPLE, 14)

    def leaveEvent(self, e):
        self._normal()
        self.setGraphicsEffect(None)

# ═══════════════════════════════════════════════════════
#  KONTENT SAHIFA
# ═══════════════════════════════════════════════════════
class ContentPage(QWidget):
    def __init__(self, category: str, parent=None):
        super().__init__(parent)
        self.category = category
        self.setStyleSheet("background: transparent;")
        self._build()

    def _build(self):
        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(20, 16, 20, 16)
        main_lay.setSpacing(20)

        games = GAMES.get(self.category, [])

        # Launcherlar (faqat "Barcha o'yinlar" da)
        if self.category == "Barcha o'yinlar":
            sec = self._section_label("LAUNCHERLAR")
            main_lay.addWidget(sec)

            lframe = QFrame()
            lframe.setStyleSheet("background: transparent;")
            l_lay = QHBoxLayout(lframe)
            l_lay.setContentsMargins(0, 0, 0, 0)
            l_lay.setSpacing(10)
            l_lay.setAlignment(Qt.AlignLeft)

            for ldata in LAUNCHERS:
                card = LauncherCard(ldata)
                l_lay.addWidget(card)
            l_lay.addStretch()
            main_lay.addWidget(lframe)

        # O'yinlar
        sec2 = self._section_label("BARCHA O'YINLAR" if self.category == "Barcha o'yinlar" else self.category.upper())
        main_lay.addWidget(sec2)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                background: #0a0a1e; width: 6px; border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #2a2a5a; border-radius: 3px; min-height: 24px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)

        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent;")
        grid = QGridLayout(grid_widget)
        grid.setSpacing(12)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        cols = 7
        for i, g in enumerate(games):
            card = GameCard(g)
            grid.addWidget(card, i // cols, i % cols)

        scroll.setWidget(grid_widget)
        main_lay.addWidget(scroll)

    def _section_label(self, text):
        row = QWidget()
        row.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(row)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        lbl = QLabel(text)
        lbl.setFont(orbitron(9))
        lbl.setStyleSheet(f"color: {C_MUTED}; letter-spacing: 3px; background: transparent;")

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"background: {C_BORDER}; border: none; max-height: 1px;")

        lay.addWidget(lbl)
        lay.addWidget(line, 1)
        return row

# ═══════════════════════════════════════════════════════
#  ASOSIY OYNA
# ═══════════════════════════════════════════════════════
class LauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COMFORTGAMECLUB")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.showFullScreen()
        self._drag_pos = None
        self._pages = {}
        self._build_ui()
        self._start_clock()

    # ── UI ──────────────────────────────────────────────
    def _build_ui(self):
        root = QWidget()
        root.setStyleSheet(f"background: {C_BG};")
        self.setCentralWidget(root)

        v = QVBoxLayout(root)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        v.addWidget(self._build_topbar())
        mid = QWidget()
        mid.setStyleSheet("background: transparent;")
        h = QHBoxLayout(mid)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)
        h.addWidget(self._build_sidebar())
        h.addWidget(self._build_content())
        v.addWidget(mid, 1)
        v.addWidget(self._build_bottombar())

    # ── TOPBAR ──────────────────────────────────────────
    def _build_topbar(self):
        bar = QFrame()
        bar.setFixedHeight(46)
        bar.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #08081c, stop:0.5 #10102a, stop:1 #08081c);
                border-bottom: 1px solid #20204a;
            }}
        """)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(16, 0, 16, 0)
        lay.setSpacing(0)

        # Logo
        logo = QLabel("🎮  COMFORTGAMECLUB")
        logo.setFont(orbitron(13))
        logo.setStyleSheet(f"""
            color: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 {C_CYAN}, stop:1 {C_PURPLE2});
            background: transparent;
            letter-spacing: 3px;
        """)
        lay.addWidget(logo)
        lay.addSpacing(30)

        # Nav tugmalar
        self._nav_btns = {}
        categories = list(GAMES.keys())
        for cat in categories:
            btn = QPushButton(cat.upper())
            btn.setFont(make_font(11, bold=True))
            btn.setFixedHeight(46)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(self._nav_style(False))
            btn.clicked.connect(lambda _, c=cat: self._switch_page(c))
            self._nav_btns[cat] = btn
            lay.addWidget(btn)

        lay.addStretch()

        # Soat
        self.clock_lbl = QLabel("00:00:00")
        self.clock_lbl.setFont(orbitron(15))
        self.clock_lbl.setStyleSheet(f"color: {C_PINK}; background: transparent; letter-spacing: 2px;")
        lay.addWidget(self.clock_lbl)

        lay.addSpacing(14)

        # Yopish
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(32, 32)
        close_btn.setFont(make_font(14, bold=True))
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba(255,45,120,0.12);
                color: {C_PINK};
                border: 1px solid rgba(255,45,120,0.3);
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background: rgba(255,45,120,0.3);
                border: 1px solid {C_PINK};
            }}
        """)
        close_btn.clicked.connect(self.close)
        lay.addWidget(close_btn)

        # Drag
        bar.mousePressEvent   = self._drag_start
        bar.mouseMoveEvent    = self._drag_move
        bar.mouseReleaseEvent = self._drag_end

        return bar

    def _nav_style(self, active):
        if active:
            return f"""
                QPushButton {{
                    color: {C_CYAN};
                    background: rgba(0,229,255,0.08);
                    border: none;
                    border-bottom: 2px solid {C_CYAN};
                    padding: 0 18px;
                    font-weight: bold;
                }}
            """
        return f"""
            QPushButton {{
                color: #666699;
                background: transparent;
                border: none;
                padding: 0 18px;
            }}
            QPushButton:hover {{
                color: #aaaadd;
                background: rgba(123,47,255,0.1);
            }}
        """

    # ── SIDEBAR ─────────────────────────────────────────
    def _build_sidebar(self):
        sb = QFrame()
        sb.setFixedWidth(54)
        sb.setStyleSheet(f"""
            QFrame {{
                background: #08081c;
                border-right: 1px solid {C_BORDER};
            }}
        """)
        lay = QVBoxLayout(sb)
        lay.setContentsMargins(6, 12, 6, 12)
        lay.setSpacing(8)
        lay.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        icons = [("🎮","Steam"),("💬","Discord"),("🌐","Chrome"),("▶️","YouTube"),("📸","Screenshots")]
        for ico, tip in icons:
            lay.addWidget(SideBtn(ico, tip))

        lay.addStretch()

        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet(f"background: {C_BORDER}; border: none;")
        lay.addWidget(line)

        lay.addWidget(SideBtn("⚙️","Sozlamalar"))
        lay.addWidget(SideBtn("👤","Profil"))
        return sb

    # ── CONTENT ─────────────────────────────────────────
    def _build_content(self):
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"""
            QStackedWidget {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 {C_BG}, stop:0.5 #0d0d22, stop:1 {C_BG});
            }}
        """)
        for cat in GAMES.keys():
            page = ContentPage(cat)
            self._pages[cat] = page
            self.stack.addWidget(page)

        # Birinchi sahifani faollashtirish
        first = list(GAMES.keys())[0]
        self._switch_page(first)
        return self.stack

    # ── BOTTOMBAR ───────────────────────────────────────
    def _build_bottombar(self):
        bar = QFrame()
        bar.setFixedHeight(50)
        bar.setStyleSheet(f"""
            QFrame {{
                background: #08081c;
                border-top: 1px solid {C_BORDER};
            }}
        """)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(16, 0, 16, 0)
        lay.setSpacing(6)

        for ico, txt in [("🎧","Audio"),("🎤","Mikrofon"),("👓","Display")]:
            btn = QPushButton(f"{ico}  {txt}")
            btn.setFont(make_font(12, bold=True))
            btn.setFixedHeight(34)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    color: {C_MUTED}; background: transparent;
                    border: none; padding: 0 12px; border-radius: 8px;
                }}
                QPushButton:hover {{
                    background: rgba(123,47,255,0.15); color: #fff;
                }}
            """)
            lay.addWidget(btn)

        div = QFrame()
        div.setFrameShape(QFrame.VLine)
        div.setFixedWidth(1)
        div.setStyleSheet(f"background: {C_BORDER}; border: none;")
        lay.addWidget(div)

        for key, desc in [("F1","yordam"),("F2","shovqin"),("F5","PRIMO sayt")]:
            tip = QLabel(f"<span style='color:#333366'>{key} — </span><span style='color:{C_PURPLE2}'>{desc}</span>")
            tip.setFont(make_font(11))
            tip.setStyleSheet("background: transparent;")
            lay.addWidget(tip)

        lay.addStretch()

        bal_frame = QFrame()
        bal_frame.setStyleSheet(f"""
            QFrame {{
                background: rgba(255,230,0,0.08);
                border: 1px solid rgba(255,230,0,0.25);
                border-radius: 18px;
                padding: 0 4px;
            }}
        """)
        b_lay = QHBoxLayout(bal_frame)
        b_lay.setContentsMargins(12, 4, 12, 4)
        b_lay.setSpacing(6)

        bal_ico = QLabel("💰")
        bal_ico.setFont(QFont("Segoe UI Emoji", 16))
        bal_ico.setStyleSheet("background: transparent; border: none;")

        self.bal_lbl = QLabel("45 so'm/min")
        self.bal_lbl.setFont(orbitron(12))
        self.bal_lbl.setStyleSheet(f"color: {C_YELLOW}; background: transparent; border: none;")

        b_lay.addWidget(bal_ico)
        b_lay.addWidget(self.bal_lbl)
        lay.addWidget(bal_frame)

        return bar

    # ── SAHIFA O'ZGARTIRISH ──────────────────────────────
    def _switch_page(self, category):
        for cat, btn in self._nav_btns.items():
            btn.setStyleSheet(self._nav_style(cat == category))
        self.stack.setCurrentWidget(self._pages[category])

    # ── SOAT ─────────────────────────────────────────────
    def _start_clock(self):
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_clock)
        self._timer.start(1000)
        self._update_clock()

    def _update_clock(self):
        self.clock_lbl.setText(datetime.now().strftime("%H:%M:%S"))

    # ── DRAG ─────────────────────────────────────────────
    def _drag_start(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_pos = e.globalPos() - self.frameGeometry().topLeft()

    def _drag_move(self, e):
        if e.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(e.globalPos() - self._drag_pos)

    def _drag_end(self, e):
        self._drag_pos = None

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.showNormal()
        elif e.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

# ═══════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    pal = QPalette()
    pal.setColor(QPalette.Window,       QColor(C_BG))
    pal.setColor(QPalette.WindowText,   QColor("#ffffff"))
    pal.setColor(QPalette.Base,         QColor(C_CARD))
    pal.setColor(QPalette.Text,         QColor("#ffffff"))
    pal.setColor(QPalette.Button,       QColor(C_CARD))
    pal.setColor(QPalette.ButtonText,   QColor("#ffffff"))
    pal.setColor(QPalette.Highlight,    QColor(C_PURPLE))
    app.setPalette(pal)

    win = LauncherWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
