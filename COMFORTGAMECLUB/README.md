# 🎮 COMFORTGAMECLUB — Boshqaruv Tizimi

## Loyiha haqida
COMFORTGAMECLUB game club uchun maxsus yaratilgan Admin + Client boshqaruv tizimi.

---

## 📁 Fayl Strukturasi
```
COMFORTGAMECLUB/
├── admin/
│   ├── admin_ui.py        ← Admin Panel (asosiy oyna)
│   └── admin_server.py    ← Server (clientlarni boshqaradi)
├── client/
│   ├── client_ui.py       ← Client oynasi (gaming menu)
│   ├── client_network.py  ← Server bilan aloqa
│   ├── blocker.py         ← Tizimni bloklash moduli
│   └── games_data.py      ← O'yinlar ro'yxati
├── shared/
│   └── protocol.py        ← Umumiy protokol
├── start_admin.bat        ← Admin ishga tushirish
├── start_client.bat       ← Client ishga tushirish
├── install.bat            ← Paketlarni o'rnatish
└── requirements.txt
```

---

## 🚀 O'rnatish va Ishga Tushirish

### 1. Talab qilinadigan dasturlar
- **Python 3.8+** — https://python.org
- Windows 10

### 2. Paketlarni o'rnatish
```
install.bat  ni ishga tushiring
```
yoki qo'lda:
```bash
pip install PyQt5 pynput
```

### 3. Admin PC da
```
start_admin.bat
```

### 4. Client PC da
```
start_client.bat
```
IP manzilni so'raganda — **Admin PC ning IP manzilini** kiriting.

---

## 🌐 Tarmoq sozlamalari

```
Admin PC (server)  ──────────────  Client PC lar
192.168.1.100:9999              192.168.1.101
                                192.168.1.102
                                192.168.1.103...
```

**Muhim:** Barcha PC lar **bir xil tarmoqda** (Wi-Fi yoki LAN) bo'lishi kerak!

Admin PC IP manzilini bilish uchun:
```
Win + R → cmd → ipconfig
```
`IPv4 Address` qatoridagi manzil — bu siz kiritadigan IP.

---

## 🔧 Admin Panel imkoniyatlari

| Tugma | Vazifa |
|-------|--------|
| 🔒 Bloklash | Tanlangan PC ni bloklaydi |
| 🔓 Blokdan chiqarish | PC ni ochadi |
| ⏱️ Vaqt belgilash | O'yin vaqtini (daqiqa) belgilaydi |
| 💬 Xabar yuborish | Client ekraniga xabar chiqaradi |
| ⏻ O'chirish | PC ni o'chiradi (10 soniyadan keyin) |
| 🔄 Qayta yoqish | PC ni qayta yoqadi |
| 🔒 Hammasini bloklash | Barcha online PC larni bloklaydi |
| 🔓 Hammasini ochish | Barcha PC larni blokdan chiqaradi |
| ⏻ Hammasini o'chirish | Barcha PC larni o'chiradi |

---

## 🎮 O'yinlar menyusi (Client)

- 🔫 **Shooter** — CS2, Valorant, COD, Apex, Fortnite, PUBG...
- 🏎️ **Gonkalar** — NFS, Forza, F1, Assetto Corsa...
- ⚔️ **Jangovar** — Tekken 8, MK1, Street Fighter 6...
- 🌍 **Ochiq dunyo** — GTA V, Cyberpunk, Elden Ring...
- 🏀 **Sport** — FIFA, NBA 2K, WWE...
- 🎲 **Boshqalar** — Minecraft, Roblox, Steam...

---

## 🔒 Bloklash tizimi

Bloklanganda:
- Butun ekran qoplanadi (qora gradient)
- 🔒 katta qulf belgisi ko'rinadi
- Klaviatura tugmalari e'tiborsiz qoldiriladi
- Task Manager o'chiriladi (registry orqali)
- Desktop kontekst menyusi o'chiriladi
- Oynani yopib bo'lmaydi

---

## ⚙️ O'yinlarni sozlash

`client/games_data.py` faylida o'yinlarni qo'shing/o'zgarting:
```python
{"name": "O'yin nomi", "exe": "oyun.exe", "icon": "🎮"},
```

---

## 📞 Yordam
Muammo bo'lsa `start_client.bat` yoki `start_admin.bat` ni **administrator sifatida** ishga tushiring.
