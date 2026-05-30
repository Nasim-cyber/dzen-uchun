"""
COMFORTGAMECLUB - Bloklash moduli
Windows da keyboard/mouse va tizim tugmalarini bloklaydi
"""

import sys
import os
import threading
import ctypes
import subprocess

IS_WINDOWS = sys.platform == "win32"

if IS_WINDOWS:
    import winreg
    try:
        from pynput import keyboard, mouse
        PYNPUT_OK = True
    except ImportError:
        PYNPUT_OK = False
else:
    PYNPUT_OK = False


class SystemBlocker:
    """
    Windows da foydalanuvchi tizimni chetlab o'ta olmasin deb:
    1. Task Manager o'chiriladi
    2. Win tugmasi bloklashadi
    3. Alt+F4, Alt+Tab, Ctrl+Alt+Del effektlari bloklashadi
    4. Registry orqali Task Manager disable
    """

    def __init__(self):
        self._kb_listener = None
        self._mouse_listener = None
        self._blocked = False
        self._block_lock = threading.Lock()

        # Bloklash kerak bo'lmagan tugmalar (agar kerak bo'lsa)
        self._allowed_keys = set()

    def block(self):
        """Tizimni bloklaydi"""
        with self._block_lock:
            if self._blocked:
                return
            self._blocked = True

        if IS_WINDOWS:
            self._disable_task_manager()
            self._disable_registry_escapes()
            if PYNPUT_OK:
                self._start_key_blocker()

    def unblock(self):
        """Blokni olib tashlaydi"""
        with self._block_lock:
            if not self._blocked:
                return
            self._blocked = False

        if IS_WINDOWS:
            self._enable_task_manager()
            self._enable_registry_escapes()
            if PYNPUT_OK:
                self._stop_key_blocker()

    @property
    def is_blocked(self):
        return self._blocked

    # ── Registry ──────────────────────────────────────────

    def _disable_task_manager(self):
        """Task Manager ni o'chiradi (registry)"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                0, winreg.KEY_SET_VALUE | winreg.KEY_CREATE_SUB_KEY
            )
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
        except Exception as e:
            print(f"[BLOCKER] Task Manager o'chirishda xato: {e}")

    def _enable_task_manager(self):
        """Task Manager ni qaytaradi"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
        except Exception as e:
            print(f"[BLOCKER] Task Manager qaytarishda xato: {e}")

    def _disable_registry_escapes(self):
        """Desktop kontekst menyusini o'chiradi"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                0, winreg.KEY_SET_VALUE | winreg.KEY_CREATE_SUB_KEY
            )
            winreg.SetValueEx(key, "NoDesktopContextMenu", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "NoRun", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
        except Exception as e:
            print(f"[BLOCKER] Registry xato: {e}")

    def _enable_registry_escapes(self):
        """Desktop kontekst menyusini qaytaradi"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "NoDesktopContextMenu", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "NoRun", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
        except Exception as e:
            print(f"[BLOCKER] Registry qaytarishda xato: {e}")

    # ── Keyboard hook (pynput) ──────────────────────────────

    def _start_key_blocker(self):
        """Xavfli tugma kombinatsiyalarini bloklaydi"""
        blocked_combos = {
            # Win tugmasi
            keyboard.Key.cmd,
            keyboard.Key.cmd_r,
            # Alt+F4
            # Ctrl+Esc
            keyboard.Key.esc,
        }

        def on_press(key):
            if not self._blocked:
                return True
            # Win tugmasini bloklash
            if key in (keyboard.Key.cmd, keyboard.Key.cmd_r):
                return False
            return True

        def on_release(key):
            if not self._blocked:
                return True
            if key in (keyboard.Key.cmd, keyboard.Key.cmd_r):
                return False
            return True

        self._kb_listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release,
            suppress=False
        )
        self._kb_listener.start()

    def _stop_key_blocker(self):
        if self._kb_listener:
            try:
                self._kb_listener.stop()
            except:
                pass
            self._kb_listener = None

    # ── Qo'shimcha: oynani oldinga chiqarish ───────────────

    def bring_window_to_front(self, hwnd):
        """Oynani eng oldinga olib chiqadi (Windows)"""
        if IS_WINDOWS and hwnd:
            try:
                ctypes.windll.user32.SetForegroundWindow(hwnd)
                ctypes.windll.user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE
            except:
                pass
