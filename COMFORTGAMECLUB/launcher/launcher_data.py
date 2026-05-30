"""
COMFORTGAMECLUB - Launcher va O'yinlar ma'lumotlari
"""

# ── LAUNCHERLAR ──────────────────────────────────────────────
LAUNCHERS = [
    {"name": "Steam",        "icon": "🎮", "color": "#1b2838", "exe": "steam.exe",                  "bg": "#1b2838"},
    {"name": "Epic Games",   "icon": "🟣", "color": "#2d1b4e", "exe": "EpicGamesLauncher.exe",       "bg": "#1c1c2e"},
    {"name": "EA Play",      "icon": "🔴", "color": "#9b0026", "exe": "EADesktop.exe",               "bg": "#2a0010"},
    {"name": "Battle.net",   "icon": "⚔️", "color": "#0066cc", "exe": "Battle.net.exe",              "bg": "#001833"},
    {"name": "Riot Games",   "icon": "⚡", "color": "#d4202a", "exe": "RiotClientServices.exe",      "bg": "#1a0005"},
    {"name": "GameLoop",     "icon": "📱", "color": "#0066cc", "exe": "GameLoop.exe",                "bg": "#001a33"},
    {"name": "FACEIT",       "icon": "🏆", "color": "#ff6600", "exe": "FACEIT.exe",                  "bg": "#1a0a00"},
    {"name": "FASTCUP",      "icon": "🏎️", "color": "#cc0000", "exe": "fastcup.exe",                 "bg": "#1a0000"},
    {"name": "Wargaming",    "icon": "🔫", "color": "#004499", "exe": "wgc.exe",                     "bg": "#00112a"},
    {"name": "Ubisoft",      "icon": "🔷", "color": "#0070cc", "exe": "UbisoftConnect.exe",          "bg": "#001a33"},
]

# ── O'YINLAR ─────────────────────────────────────────────────
GAMES = {
    "Barcha o'yinlar": [
        # SHOOTER
        {"name": "Counter-Strike 2",      "genre": "Tactical FPS",  "icon": "💣", "color": "#ff8c00", "exe": "cs2.exe",                           "badge": "HOT"},
        {"name": "Valorant",              "genre": "Tactical FPS",  "icon": "⚡", "color": "#ff2d78", "exe": "VALORANT.exe",                       "badge": "HOT"},
        {"name": "Apex Legends",          "genre": "Battle Royale", "icon": "🦊", "color": "#cc4400", "exe": "r5apex.exe",                         "badge": "TOP"},
        {"name": "COD: Warzone",          "genre": "Battle Royale", "icon": "🪖", "color": "#556600", "exe": "cod.exe",                            "badge": ""},
        {"name": "PUBG",                  "genre": "Battle Royale", "icon": "🪂", "color": "#775500", "exe": "TslGame.exe",                        "badge": ""},
        {"name": "Rainbow Six Siege",     "genre": "Tactical FPS",  "icon": "🛡️", "color": "#003388", "exe": "RainbowSix.exe",                    "badge": ""},
        {"name": "Battlefield V",         "genre": "FPS Shooter",   "icon": "🪖", "color": "#445566", "exe": "bfv.exe",                            "badge": ""},
        {"name": "COD: Black Ops 2",      "genre": "FPS Shooter",   "icon": "🔫", "color": "#333333", "exe": "t6mp.exe",                           "badge": "TOP"},
        {"name": "COD: Black Ops 3",      "genre": "FPS Shooter",   "icon": "💀", "color": "#222233", "exe": "BlackOps3.exe",                      "badge": ""},
        # GONKALAR
        {"name": "Need for Speed Heat",   "genre": "Racing",        "icon": "🔥", "color": "#cc3300", "exe": "NeedForSpeedHeat.exe",               "badge": ""},
        {"name": "Forza Horizon 5",       "genre": "Racing",        "icon": "🏎️", "color": "#cc6600", "exe": "ForzaHorizon5.exe",                 "badge": "TOP"},
        {"name": "Blur",                  "genre": "Racing",        "icon": "💨", "color": "#005533", "exe": "blur.exe",                           "badge": ""},
        {"name": "Assetto Corsa",         "genre": "Sim Racing",    "icon": "🚗", "color": "#333300", "exe": "acs.exe",                            "badge": ""},
        {"name": "F1 2024",               "genre": "Sim Racing",    "icon": "🏁", "color": "#cc0033", "exe": "F1_2024.exe",                        "badge": "NEW"},
        # OCHIQ DUNYO
        {"name": "GTA V",                 "genre": "Open World",    "icon": "🌆", "color": "#003322", "exe": "GTA5.exe",                           "badge": "TOP"},
        {"name": "RDR 2",                 "genre": "Open World",    "icon": "🤠", "color": "#442200", "exe": "RDR2.exe",                           "badge": ""},
        {"name": "Cyberpunk 2077",        "genre": "RPG",           "icon": "🤖", "color": "#003344", "exe": "Cyberpunk2077.exe",                  "badge": "NEW"},
        {"name": "The Witcher 3",         "genre": "RPG",           "icon": "🐺", "color": "#223300", "exe": "witcher3.exe",                       "badge": ""},
        {"name": "Elden Ring",            "genre": "Action RPG",    "icon": "⚔️", "color": "#332200", "exe": "eldenring.exe",                     "badge": "TOP"},
        # JANGOVAR
        {"name": "Mortal Kombat 1",       "genre": "Fighting",      "icon": "💀", "color": "#440000", "exe": "MK1.exe",                            "badge": "NEW"},
        {"name": "Tekken 8",              "genre": "Fighting",      "icon": "🥊", "color": "#222244", "exe": "Tekken8.exe",                        "badge": "NEW"},
        {"name": "Street Fighter 6",      "genre": "Fighting",      "icon": "👊", "color": "#440022", "exe": "StreetFighter6.exe",                 "badge": ""},
        # SPORT
        {"name": "EA Sports FC 24",       "genre": "Football",      "icon": "⚽", "color": "#003300", "exe": "FC24.exe",                           "badge": "HOT"},
        {"name": "NBA 2K24",              "genre": "Basketball",    "icon": "🏀", "color": "#442200", "exe": "NBA2K24.exe",                        "badge": ""},
        {"name": "WWE 2K24",              "genre": "Wrestling",     "icon": "🤼", "color": "#330022", "exe": "WWE2K24.exe",                        "badge": ""},
        # BOSHQALAR
        {"name": "Minecraft",             "genre": "Sandbox",       "icon": "⛏️", "color": "#225500", "exe": "javaw.exe",                         "badge": ""},
        {"name": "Roblox",                "genre": "Sandbox",       "icon": "🧱", "color": "#004488", "exe": "RobloxPlayerBeta.exe",               "badge": ""},
        {"name": "Generals: Zero Hour",   "genre": "Strategy",      "icon": "💥", "color": "#443300", "exe": "game.dat",                           "badge": "TOP"},
        {"name": "Age of Empires IV",     "genre": "Strategy",      "icon": "🏰", "color": "#442200", "exe": "AgeOfEmpires4.exe",                  "badge": ""},
    ],
    "Onlayn o'yinlar": [],
    "Counter-Strike": [],
    "Dasturlar": [
        {"name": "Google Chrome",         "genre": "Brauzer",       "icon": "🌐", "color": "#004488", "exe": "chrome.exe",                         "badge": ""},
        {"name": "Discord",               "genre": "Chatting",      "icon": "💬", "color": "#223388", "exe": "Discord.exe",                        "badge": ""},
        {"name": "Telegram",              "genre": "Chatting",      "icon": "✈️", "color": "#003366", "exe": "Telegram.exe",                      "badge": ""},
        {"name": "VLC Player",            "genre": "Media",         "icon": "🎬", "color": "#662200", "exe": "vlc.exe",                            "badge": ""},
        {"name": "TeamViewer",            "genre": "Remote",        "icon": "🖥️", "color": "#003388", "exe": "TeamViewer.exe",                    "badge": ""},
    ],
    "Internet": [
        {"name": "Google Chrome",         "genre": "Brauzer",       "icon": "🌐", "color": "#004488", "exe": "chrome.exe",                         "badge": ""},
        {"name": "YouTube",               "genre": "Video",         "icon": "▶️", "color": "#440000", "exe": "chrome.exe --app=https://youtube.com","badge": ""},
        {"name": "Twitch",                "genre": "Streaming",     "icon": "🟣", "color": "#330055", "exe": "chrome.exe --app=https://twitch.tv",  "badge": ""},
    ],
}

# Onlayn va CS o'yinlarni filter qilish
GAMES["Onlayn o'yinlar"] = [g for g in GAMES["Barcha o'yinlar"] if g["genre"] in ("Tactical FPS","Battle Royale","FPS Shooter")]
GAMES["Counter-Strike"]  = [g for g in GAMES["Barcha o'yinlar"] if "Counter-Strike" in g["name"] or "Valorant" in g["name"] or "Siege" in g["name"]]
