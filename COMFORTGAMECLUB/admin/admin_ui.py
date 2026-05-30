"""
COMFORTGAMECLUB - Admin Panel UI
PyQt5 bilan yaratilgan zamonaviy boshqaruv paneli
"""

import sys
import os
import socket
import threading
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QFrame, QMessageBox, QInputDialog, QSpinBox, QDialog,
    QDialogButtonBox, QGridLayout, QGroupBox, QStatusBar, QSplitter,
    QToolButton, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize
from PyQt5.QtGui import (
    QColor, QFont, QPalette, QIcon, QPixmap, QPainter,
    QLinearGradient, QBrush
)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.protocol import SERVER_PORT
from admin_server import AdminServer, ClientInfo


# ===== RANGLAR =====
BG_DARK      = "#0a0a1a"
BG_CARD      = "#12122a"
BG_HEADER    = "#0d0d2b"
ACCENT_CYAN  = "#00e5ff"
ACCENT_BLUE  = "#1a6fff"
ACCENT_PINK  = "#ff2d78"
ACCENT_GREEN = "#00ff88"
ACCENT_ORANGE= "#ff8c00"
TEXT_WHITE   = "#ffffff"
TEXT_GRAY    = "#8888aa"
BORDER_COLOR = "#1e1e4a"
ROW_ODD      = "#0f0f25"
ROW_EVEN     = "#13132e"
STATUS_ONLINE  = "#00ff88"
STATUS_BLOCKED = "#ff2d78"
STATUS_OFFLINE = "#555577"


STYLE_MAIN = f"""
QMainWindow, QWidget {{
    background-color: {BG_DARK};
    color: {TEXT_WHITE};
    font-family: 'Segoe UI', Arial;
}}

QTableWidget {{
    background-color: {BG_CARD};
    color: {TEXT_WHITE};
    gridline-color: {BORDER_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    font-size: 13px;
    selection-background-color: {ACCENT_BLUE};
}}
QTableWidget::item {{
    padding: 6px 10px;
}}
QTableWidget::item:selected {{
    background-color: {ACCENT_BLUE}44;
}}
QHeaderView::section {{
    background-color: {BG_HEADER};
    color: {ACCENT_CYAN};
    font-weight: bold;
    font-size: 12px;
    padding: 8px;
    border: none;
    border-bottom: 2px solid {ACCENT_BLUE};
}}

QPushButton {{
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 12px;
    border: none;
    color: white;
}}

QStatusBar {{
    background-color: {BG_HEADER};
    color: {TEXT_GRAY};
    font-size: 11px;
    border-top: 1px solid {BORDER_COLOR};
}}

QGroupBox {{
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    margin-top: 14px;
    padding: 10px;
    color: {ACCENT_CYAN};
    font-weight: bold;
    font-size: 12px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: {ACCENT_CYAN};
}}

QInputDialog, QMessageBox {{
    background-color: {BG_DARK};
    color: white;
}}
QSpinBox {{
    background-color: {BG_CARD};
    color: white;
    border: 1px solid {BORDER_COLOR};
    border-radius: 4px;
    padding: 4px 8px;
}}
"""


def btn_style(color):
    return f"""
    QPushButton {{
        background-color: {color}22;
        color: {color};
        border: 1px solid {color}66;
        border-radius: 6px;
        padding: 7px 14px;
        font-weight: bold;
        font-size: 12px;
    }}
    QPushButton:hover {{
        background-color: {color}44;
        border: 1px solid {color};
    }}
    QPushButton:pressed {{
        background-color: {color}66;
    }}
    QPushButton:disabled {{
        background-color: #1a1a2e;
        color: #444466;
        border: 1px solid #222244;
    }}
    """


class PcCard(QFrame):
    """Har bir PC uchun karta"""
    def __init__(self, info: ClientInfo, parent=None):
        super().__init__(parent)
        self.info = info
        self._build()

    def _build(self):
        self.setFixedSize(180, 120)
        self.setFrameShape(QFrame.StyledPanel)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(4)

        # PC nomi
        name_lbl = QLabel(self.info.pc_name)
        name_lbl.setAlignment(Qt.AlignCenter)
        name_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        name_lbl.setStyleSheet(f"color: {ACCENT_CYAN};")
        layout.addWidget(name_lbl)

        # IP
        ip_lbl = QLabel(self.info.ip)
        ip_lbl.setAlignment(Qt.AlignCenter)
        ip_lbl.setStyleSheet(f"color: {TEXT_GRAY}; font-size: 10px;")
        layout.addWidget(ip_lbl)

        # Status
        status = self.info.status
        if status == "online":
            color = STATUS_ONLINE
            text = "● ONLINE"
        elif status == "blocked":
            color = STATUS_BLOCKED
            text = "🔒 BLOKLANGAN"
        else:
            color = STATUS_OFFLINE
            text = "○ OFFLINE"

        st_lbl = QLabel(text)
        st_lbl.setAlignment(Qt.AlignCenter)
        st_lbl.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 11px;")
        layout.addWidget(st_lbl)

        # Border rangi
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_CARD};
                border: 1px solid {color}66;
                border-radius: 10px;
            }}
            QFrame:hover {{
                border: 1px solid {color};
            }}
        """)


class AdminWindow(QMainWindow):
    update_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.server = AdminServer(on_update=self._on_server_update)
        self.selected_pc = None

        self.setWindowTitle("COMFORTGAMECLUB — Admin Panel")
        self.setMinimumSize(1100, 700)
        self.setStyleSheet(STYLE_MAIN)

        self._build_ui()
        self.update_signal.connect(self._refresh_table)

        # Server ishga tushirish
        self._start_server()

        # Auto refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._refresh_table)
        self.timer.start(3000)

    # ─────────────────── UI QURILISHI ───────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        main_layout.addWidget(self._build_header())

        # Kontent
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(12)

        # Chap: jadval
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        # Statistika
        left_layout.addWidget(self._build_stats())

        # Jadval
        left_layout.addWidget(self._build_table())

        content_layout.addWidget(left, stretch=3)

        # O'ng: boshqaruv
        content_layout.addWidget(self._build_control_panel(), stretch=1)

        main_layout.addWidget(content)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Server ishga tushirilmoqda...")

    def _build_header(self):
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0d0d2b,
                    stop:0.5 #0a1550,
                    stop:1 #0d0d2b
                );
                border-bottom: 2px solid {ACCENT_BLUE};
            }}
        """)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)

        # Logo + Nom
        logo_layout = QHBoxLayout()
        icon_lbl = QLabel("🎮")
        icon_lbl.setFont(QFont("Segoe UI", 28))
        logo_layout.addWidget(icon_lbl)

        name_layout = QVBoxLayout()
        title = QLabel("COMFORTGAMECLUB")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet(f"color: {ACCENT_CYAN}; letter-spacing: 3px;")
        subtitle = QLabel("ADMIN BOSHQARUV PANELI")
        subtitle.setFont(QFont("Segoe UI", 9))
        subtitle.setStyleSheet(f"color: {TEXT_GRAY}; letter-spacing: 2px;")
        name_layout.addWidget(title)
        name_layout.addWidget(subtitle)
        logo_layout.addLayout(name_layout)
        layout.addLayout(logo_layout)

        layout.addStretch()

        # Server IP
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
        except:
            local_ip = "127.0.0.1"

        ip_frame = QFrame()
        ip_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_CARD};
                border: 1px solid {BORDER_COLOR};
                border-radius: 8px;
                padding: 4px 12px;
            }}
        """)
        ip_layout = QVBoxLayout(ip_frame)
        ip_layout.setContentsMargins(8, 4, 8, 4)
        ip_layout.setSpacing(2)
        ip_label = QLabel(f"Server IP: {local_ip}")
        ip_label.setStyleSheet(f"color: {ACCENT_GREEN}; font-weight: bold; font-size: 12px;")
        port_label = QLabel(f"Port: {SERVER_PORT}")
        port_label.setStyleSheet(f"color: {TEXT_GRAY}; font-size: 10px;")
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(port_label)
        layout.addWidget(ip_frame)

        return header

    def _build_stats(self):
        frame = QFrame()
        frame.setStyleSheet(f"background: transparent;")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.stat_total  = self._stat_card("JAMI", "0", ACCENT_CYAN)
        self.stat_online = self._stat_card("ONLINE", "0", ACCENT_GREEN)
        self.stat_blocked= self._stat_card("BLOKLANGAN", "0", ACCENT_PINK)
        self.stat_offline= self._stat_card("OFFLINE", "0", STATUS_OFFLINE)

        layout.addWidget(self.stat_total)
        layout.addWidget(self.stat_online)
        layout.addWidget(self.stat_blocked)
        layout.addWidget(self.stat_offline)
        return frame

    def _stat_card(self, label, value, color):
        frame = QFrame()
        frame.setFixedHeight(70)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_CARD};
                border: 1px solid {color}44;
                border-left: 3px solid {color};
                border-radius: 8px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(2)

        val_lbl = QLabel(value)
        val_lbl.setFont(QFont("Segoe UI", 22, QFont.Bold))
        val_lbl.setStyleSheet(f"color: {color};")
        val_lbl.setAlignment(Qt.AlignCenter)

        txt_lbl = QLabel(label)
        txt_lbl.setFont(QFont("Segoe UI", 9))
        txt_lbl.setStyleSheet(f"color: {TEXT_GRAY};")
        txt_lbl.setAlignment(Qt.AlignCenter)

        layout.addWidget(val_lbl)
        layout.addWidget(txt_lbl)

        # value labelni saqlash
        frame._value_label = val_lbl
        return frame

    def _build_table(self):
        group = QGroupBox("🖥️  Ulangan PC lar")
        layout = QVBoxLayout(group)
        layout.setSpacing(6)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "PC Nomi", "IP Manzil", "Holat", "Vaqt", "Ulanish", "Oxirgi faollik"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(True)
        self.table.clicked.connect(self._on_row_click)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                alternate-background-color: {ROW_ODD};
                background-color: {ROW_EVEN};
            }}
        """)

        layout.addWidget(self.table)
        return group

    def _build_control_panel(self):
        panel = QFrame()
        panel.setFixedWidth(260)
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_CARD};
                border: 1px solid {BORDER_COLOR};
                border-radius: 10px;
            }}
        """)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Tanlangan PC
        sel_group = QGroupBox("🎯 Tanlangan PC")
        sel_layout = QVBoxLayout(sel_group)
        self.selected_label = QLabel("Hech kim tanlanmagan")
        self.selected_label.setAlignment(Qt.AlignCenter)
        self.selected_label.setStyleSheet(f"color: {TEXT_GRAY}; font-size: 12px; padding: 6px;")
        sel_layout.addWidget(self.selected_label)
        layout.addWidget(sel_group)

        # Alohida boshqaruv
        single_group = QGroupBox("⚡ Alohida PC")
        single_layout = QVBoxLayout(single_group)
        single_layout.setSpacing(6)

        self.btn_block   = self._make_btn("🔒  Bloklash",      ACCENT_PINK,   self._block_selected)
        self.btn_unblock = self._make_btn("🔓  Blokdan chiqarish", ACCENT_GREEN, self._unblock_selected)
        self.btn_time    = self._make_btn("⏱️  Vaqt belgilash",  ACCENT_CYAN,   self._set_time_selected)
        self.btn_msg     = self._make_btn("💬  Xabar yuborish",  ACCENT_BLUE,   self._send_msg_selected)
        self.btn_shutdown= self._make_btn("⏻  O'chirish",       ACCENT_ORANGE,  self._shutdown_selected)
        self.btn_restart = self._make_btn("🔄  Qayta yoqish",   "#aa44ff",     self._restart_selected)

        for btn in [self.btn_block, self.btn_unblock, self.btn_time,
                    self.btn_msg, self.btn_shutdown, self.btn_restart]:
            single_layout.addWidget(btn)
            btn.setEnabled(False)

        layout.addWidget(single_group)

        # Hammasi boshqaruv
        all_group = QGroupBox("🌐 BARCHA PC lar")
        all_layout = QVBoxLayout(all_group)
        all_layout.setSpacing(6)

        btn_block_all   = self._make_btn("🔒  Hammasini bloklash",  ACCENT_PINK,   self._block_all)
        btn_unblock_all = self._make_btn("🔓  Hammasini ochish",    ACCENT_GREEN,  self._unblock_all)
        btn_shutdown_all= self._make_btn("⏻  Hammasini o'chirish", ACCENT_ORANGE,  self._shutdown_all)

        for btn in [btn_block_all, btn_unblock_all, btn_shutdown_all]:
            all_layout.addWidget(btn)

        layout.addWidget(all_group)
        layout.addStretch()

        # Versiya
        ver = QLabel("v1.0  •  COMFORTGAMECLUB")
        ver.setAlignment(Qt.AlignCenter)
        ver.setStyleSheet(f"color: {TEXT_GRAY}; font-size: 10px;")
        layout.addWidget(ver)

        return panel

    def _make_btn(self, text, color, slot):
        btn = QPushButton(text)
        btn.setStyleSheet(btn_style(color))
        btn.setFixedHeight(36)
        btn.clicked.connect(slot)
        return btn

    # ─────────────────── SERVER ───────────────────

    def _start_server(self):
        try:
            self.server.start()
            try:
                local_ip = socket.gethostbyname(socket.gethostname())
            except:
                local_ip = "127.0.0.1"
            self.status_bar.showMessage(
                f"✅  Server ishlamoqda  |  IP: {local_ip}  |  Port: {SERVER_PORT}  |  "
                f"Clientlar shu IP ga ulanadilar"
            )
        except Exception as e:
            self.status_bar.showMessage(f"❌  Server xatosi: {e}")
            QMessageBox.critical(self, "Xato", f"Server ishga tushmadi:\n{e}")

    def _on_server_update(self):
        self.update_signal.emit()

    # ─────────────────── JADVAL YANGILASH ───────────────────

    def _refresh_table(self):
        clients = self.server.get_clients()
        self.table.setRowCount(len(clients))

        total = len(clients)
        online = sum(1 for c in clients if c.status == "online")
        blocked = sum(1 for c in clients if c.status == "blocked")
        offline = sum(1 for c in clients if c.status == "offline")

        self.stat_total._value_label.setText(str(total))
        self.stat_online._value_label.setText(str(online))
        self.stat_blocked._value_label.setText(str(blocked))
        self.stat_offline._value_label.setText(str(offline))

        for row, c in enumerate(clients):
            # PC nomi
            self.table.setItem(row, 0, self._cell(c.pc_name, bold=True))
            # IP
            self.table.setItem(row, 1, self._cell(c.ip))
            # Holat
            if c.status == "online":
                st_item = self._cell("● ONLINE", color=STATUS_ONLINE, bold=True)
            elif c.status == "blocked":
                st_item = self._cell("🔒 BLOKLANGAN", color=STATUS_BLOCKED, bold=True)
            else:
                st_item = self._cell("○ OFFLINE", color=STATUS_OFFLINE)
            self.table.setItem(row, 2, st_item)
            # Vaqt
            if c.time_left > 0:
                t_str = f"{c.time_left} daq"
            else:
                t_str = "—"
            self.table.setItem(row, 3, self._cell(t_str))
            # Ulanish vaqti
            elapsed = int(time.time() - c.connected_at)
            h, m = divmod(elapsed // 60, 60)
            self.table.setItem(row, 4, self._cell(f"{h:02d}:{m:02d}"))
            # Oxirgi faollik
            ago = int(time.time() - c.last_seen)
            if ago < 60:
                ago_str = f"{ago}s oldin"
            else:
                ago_str = f"{ago//60}daq oldin"
            self.table.setItem(row, 5, self._cell(ago_str))

            self.table.setRowHeight(row, 40)

    def _cell(self, text, color=None, bold=False):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignCenter)
        if color:
            item.setForeground(QColor(color))
        if bold:
            f = item.font()
            f.setBold(True)
            item.setFont(f)
        return item

    def _on_row_click(self, index):
        row = index.row()
        clients = self.server.get_clients()
        if 0 <= row < len(clients):
            self.selected_pc = clients[row].pc_name
            self.selected_label.setText(f"🖥️  {self.selected_pc}")
            self.selected_label.setStyleSheet(f"color: {ACCENT_CYAN}; font-weight: bold; font-size: 13px;")
            for btn in [self.btn_block, self.btn_unblock, self.btn_time,
                        self.btn_msg, self.btn_shutdown, self.btn_restart]:
                btn.setEnabled(True)

    # ─────────────────── ALOHIDA PC BUYRUQLARI ───────────────────

    def _block_selected(self):
        if not self.selected_pc:
            return
        mins, ok = QInputDialog.getInt(self, "Bloklash", "Necha daqiqa? (0 = cheksiz):", 0, 0, 999)
        if ok:
            self.server.block_pc(self.selected_pc, mins)
            self.status_bar.showMessage(f"🔒  {self.selected_pc} bloklandi ({mins} daq)")

    def _unblock_selected(self):
        if self.selected_pc:
            self.server.unblock_pc(self.selected_pc)
            self.status_bar.showMessage(f"🔓  {self.selected_pc} blokdan chiqarildi")

    def _set_time_selected(self):
        if not self.selected_pc:
            return
        mins, ok = QInputDialog.getInt(self, "Vaqt", "O'yin vaqti (daqiqa):", 60, 1, 600)
        if ok:
            self.server.set_time(self.selected_pc, mins)
            self.status_bar.showMessage(f"⏱️  {self.selected_pc} uchun {mins} daq vaqt belgilandi")

    def _send_msg_selected(self):
        if not self.selected_pc:
            return
        text, ok = QInputDialog.getText(self, "Xabar yuborish",
                                         f"{self.selected_pc} ga xabar:")
        if ok and text:
            self.server.send_message(self.selected_pc, text)
            self.status_bar.showMessage(f"💬  {self.selected_pc} ga xabar yuborildi")

    def _shutdown_selected(self):
        if not self.selected_pc:
            return
        reply = QMessageBox.question(self, "O'chirish",
                                      f"{self.selected_pc} ni o'chirishni tasdiqlaysizmi?",
                                      QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.server.shutdown_pc(self.selected_pc)
            self.status_bar.showMessage(f"⏻  {self.selected_pc} o'chirilmoqda...")

    def _restart_selected(self):
        if not self.selected_pc:
            return
        reply = QMessageBox.question(self, "Qayta yoqish",
                                      f"{self.selected_pc} ni qayta yoqishni tasdiqlaysizmi?",
                                      QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.server.restart_pc(self.selected_pc)
            self.status_bar.showMessage(f"🔄  {self.selected_pc} qayta yoqilmoqda...")

    # ─────────────────── HAMMASI BUYRUQLARI ───────────────────

    def _block_all(self):
        reply = QMessageBox.question(self, "Bloklash",
                                      "Barcha PC larni bloklashni tasdiqlaysizmi?",
                                      QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.server.block_all()
            self.status_bar.showMessage("🔒  Barcha PC lar bloklandi")

    def _unblock_all(self):
        self.server.unblock_all()
        self.status_bar.showMessage("🔓  Barcha PC lar blokdan chiqarildi")

    def _shutdown_all(self):
        reply = QMessageBox.question(self, "O'chirish",
                                      "Barcha PC larni o'chirishni tasdiqlaysizmi?",
                                      QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.server.shutdown_all()
            self.status_bar.showMessage("⏻  Barcha PC lar o'chirilmoqda...")

    def closeEvent(self, event):
        self.server.stop()
        event.accept()


# ─────────────────── MAIN ───────────────────

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BG_DARK))
    palette.setColor(QPalette.WindowText, QColor(TEXT_WHITE))
    palette.setColor(QPalette.Base, QColor(BG_CARD))
    palette.setColor(QPalette.AlternateBase, QColor(ROW_ODD))
    palette.setColor(QPalette.Text, QColor(TEXT_WHITE))
    palette.setColor(QPalette.Button, QColor(BG_CARD))
    palette.setColor(QPalette.ButtonText, QColor(TEXT_WHITE))
    palette.setColor(QPalette.Highlight, QColor(ACCENT_BLUE))
    app.setPalette(palette)

    win = AdminWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
