"""
COMFORTGAMECLUB - Client tarmoq moduli
Admin serverga ulanadi va buyruqlarni qabul qiladi
"""

import socket
import threading
import time
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.protocol import *


class ClientNetwork:
    def __init__(self, callbacks: dict):
        """
        callbacks: {
            'on_block': fn(minutes),
            'on_unblock': fn(),
            'on_shutdown': fn(),
            'on_restart': fn(),
            'on_message': fn(text),
            'on_set_time': fn(minutes),
            'on_connect': fn(),
            'on_disconnect': fn(),
        }
        """
        self.callbacks = callbacks
        self.sock = None
        self.connected = False
        self.running = False
        self.pc_name = os.environ.get("COMPUTERNAME", socket.gethostname())
        self.is_blocked = False
        self.time_left = 0
        self._reconnect_thread = None

    def start(self, host: str, port: int = SERVER_PORT):
        self.host = host
        self.port = port
        self.running = True
        self._reconnect_thread = threading.Thread(
            target=self._reconnect_loop, daemon=True)
        self._reconnect_thread.start()

    def stop(self):
        self.running = False
        self.connected = False
        if self.sock:
            try:
                self.sock.close()
            except:
                pass

    def _reconnect_loop(self):
        while self.running:
            if not self.connected:
                try:
                    self._connect()
                except Exception as e:
                    print(f"[CLIENT] Ulanib bo'lmadi: {e}. 5s kutilmoqda...")
                    time.sleep(5)
            else:
                time.sleep(1)

    def _connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.sock.connect((self.host, self.port))
        self.sock.settimeout(None)
        self.connected = True

        # HELLO yuborish
        self.sock.sendall(encode({
            "cmd": RESP_HELLO,
            "pc_name": self.pc_name,
            "is_blocked": self.is_blocked
        }))

        cb = self.callbacks.get("on_connect")
        if cb:
            cb()

        # Xabarlarni tinglash
        self._listen()

    def _listen(self):
        buffer = ""
        try:
            while self.connected and self.running:
                chunk = self.sock.recv(4096).decode("utf-8")
                if not chunk:
                    break
                buffer += chunk
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        self._handle(decode(line))
        except Exception as e:
            print(f"[CLIENT] Aloqa uzildi: {e}")
        finally:
            self.connected = False
            cb = self.callbacks.get("on_disconnect")
            if cb:
                cb()

    def _handle(self, data: dict):
        cmd = data.get("cmd")

        if cmd == CMD_BLOCK:
            self.is_blocked = True
            minutes = data.get("minutes", 0)
            self.time_left = minutes
            cb = self.callbacks.get("on_block")
            if cb:
                cb(minutes)

        elif cmd == CMD_UNBLOCK:
            self.is_blocked = False
            self.time_left = 0
            cb = self.callbacks.get("on_unblock")
            if cb:
                cb()

        elif cmd == CMD_SHUTDOWN:
            cb = self.callbacks.get("on_shutdown")
            if cb:
                cb()

        elif cmd == CMD_RESTART:
            cb = self.callbacks.get("on_restart")
            if cb:
                cb()

        elif cmd == CMD_MESSAGE:
            text = data.get("text", "")
            cb = self.callbacks.get("on_message")
            if cb:
                cb(text)

        elif cmd == CMD_SET_TIME:
            minutes = data.get("minutes", 0)
            self.time_left = minutes
            cb = self.callbacks.get("on_set_time")
            if cb:
                cb(minutes)

        elif cmd == CMD_PING:
            self._send({"cmd": "PONG"})

    def _send(self, data: dict):
        try:
            if self.sock and self.connected:
                self.sock.sendall(encode(data))
        except:
            self.connected = False

    def send_status(self):
        self._send({
            "cmd": RESP_STATUS,
            "is_blocked": self.is_blocked,
            "time_left": self.time_left
        })
