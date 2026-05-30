# Shared protocol - Admin va Client o'rtasidagi xabarlar
import json

# Port
SERVER_PORT = 9999
SERVER_HOST = "0.0.0.0"  # Admin server barcha ulanishlarni qabul qiladi

# Buyruqlar
CMD_BLOCK = "BLOCK"          # PC ni bloklash
CMD_UNBLOCK = "UNBLOCK"      # Blokdan chiqarish
CMD_SHUTDOWN = "SHUTDOWN"    # PC ni o'chirish
CMD_RESTART = "RESTART"      # PC ni qayta yoqish
CMD_STATUS = "STATUS"        # Holat so'rash
CMD_SET_TIME = "SET_TIME"    # Vaqt belgilash (daqiqada)
CMD_MESSAGE = "MESSAGE"      # Xabar yuborish
CMD_PING = "PING"            # Aloqa tekshirish

# Client javoblari
RESP_OK = "OK"
RESP_ERROR = "ERROR"
RESP_STATUS = "STATUS_REPORT"
RESP_HELLO = "HELLO"         # Client ulanganida yuboradi


def encode(data: dict) -> bytes:
    return (json.dumps(data) + "\n").encode("utf-8")


def decode(raw: str) -> dict:
    return json.loads(raw.strip())
