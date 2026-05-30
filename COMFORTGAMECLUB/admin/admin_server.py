"""
COMFORTGAMECLUB - Admin Server
Clientlardan ulanishlarni qabul qiladi va buyruqlarni yuboradi.
"""

import socket
import threading
import json
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.protocol import *


class ClientInfo:
    def __init__(self, conn, addr, pc_name="Unknown"):
        self.conn = conn
        self.addr = addr
        self.pc_name = pc_name
        self.ip = addr[0]
        self.port = addr[1]
        self.status = "online"       # online / blocked / offline
        self.is_blocked = False
        self.time_left = 0           # daqiqada
        self.connected_at = time.time()
        self.last_seen = time.time()

    def send(self, data: dict):
        try:
            self.conn.sendall(encode(data))
            return True
        except Exception:
            self.status = "offline"
            return False


class AdminServer:
    def __init__(self, on_update=None):
        self.clients: dict[str, ClientInfo] = {}  # pc_name -> ClientInfo
        self.lock = threading.Lock()
        self.on_update = on_update  # UI yangilash callback
        self.running = False
        self.server_sock = None

    def start(self, host=SERVER_HOST, port=SERVER_PORT):
        self.running = True
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((host, port))
        self.server_sock.listen(50)
        t = threading.Thread(target=self._accept_loop, daemon=True)
        t.start()
        print(f"[SERVER] Ishga tushdi. Port: {port}")

    def stop(self):
        self.running = False
        if self.server_sock:
            self.server_sock.close()

    def _accept_loop(self):
        while self.running:
            try:
                conn, addr = self.server_sock.accept()
                t = threading.Thread(target=self._handle_client,
                                     args=(conn, addr), daemon=True)
                t.start()
            except Exception:
                break

    def _handle_client(self, conn, addr):
        info = ClientInfo(conn, addr)
        try:
            # Birinchi xabar - HELLO
            conn.settimeout(10)
            raw = conn.recv(4096).decode("utf-8")
            data = decode(raw)
            if data.get("cmd") == RESP_HELLO:
                info.pc_name = data.get("pc_name", addr[0])
                info.is_blocked = data.get("is_blocked", False)
                info.status = "blocked" if info.is_blocked else "online"
            conn.settimeout(None)
        except Exception:
            conn.close()
            return

        with self.lock:
            self.clients[info.pc_name] = info

        self._notify()

        # Xabarlarni tinglash
        buffer = ""
        try:
            while True:
                chunk = conn.recv(4096).decode("utf-8")
                if not chunk:
                    break
                buffer += chunk
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        self._process_message(info, decode(line))
        except Exception:
            pass
        finally:
            info.status = "offline"
            self._notify()

    def _process_message(self, info: ClientInfo, data: dict):
        info.last_seen = time.time()
        cmd = data.get("cmd")
        if cmd == RESP_STATUS:
            info.is_blocked = data.get("is_blocked", info.is_blocked)
            info.time_left = data.get("time_left", 0)
            info.status = "blocked" if info.is_blocked else "online"
            self._notify()
        elif cmd == "PONG":
            info.last_seen = time.time()

    def _notify(self):
        if self.on_update:
            self.on_update()

    # === Admin buyruqlari ===

    def block_pc(self, pc_name: str, minutes: int = 0):
        c = self.clients.get(pc_name)
        if c:
            c.send({"cmd": CMD_BLOCK, "minutes": minutes})

    def unblock_pc(self, pc_name: str):
        c = self.clients.get(pc_name)
        if c:
            c.send({"cmd": CMD_UNBLOCK})

    def shutdown_pc(self, pc_name: str):
        c = self.clients.get(pc_name)
        if c:
            c.send({"cmd": CMD_SHUTDOWN})

    def restart_pc(self, pc_name: str):
        c = self.clients.get(pc_name)
        if c:
            c.send({"cmd": CMD_RESTART})

    def send_message(self, pc_name: str, msg: str):
        c = self.clients.get(pc_name)
        if c:
            c.send({"cmd": CMD_MESSAGE, "text": msg})

    def set_time(self, pc_name: str, minutes: int):
        c = self.clients.get(pc_name)
        if c:
            c.send({"cmd": CMD_SET_TIME, "minutes": minutes})

    def block_all(self):
        for c in self.clients.values():
            if c.status != "offline":
                c.send({"cmd": CMD_BLOCK, "minutes": 0})

    def unblock_all(self):
        for c in self.clients.values():
            if c.status != "offline":
                c.send({"cmd": CMD_UNBLOCK})

    def shutdown_all(self):
        for c in self.clients.values():
            if c.status != "offline":
                c.send({"cmd": CMD_SHUTDOWN})

    def get_clients(self):
        with self.lock:
            return list(self.clients.values())
