"""
App catalog for AURA simulator.
Defines 20 realistic Android apps with memory and session characteristics.
"""

# Each app entry: name, category, avg_session_duration (seconds), avg_memory_mb
APP_CATALOG = [
    # ── Work ────────────────────────────────────────────────────────────────
    {"name": "Gmail",          "category": "Work",    "avg_session_duration": 180,  "avg_memory_mb": 120},
    {"name": "Slack",          "category": "Work",    "avg_session_duration": 300,  "avg_memory_mb": 180},
    {"name": "Google Meet",    "category": "Work",    "avg_session_duration": 2700, "avg_memory_mb": 350},
    {"name": "Microsoft Teams","category": "Work",    "avg_session_duration": 2400, "avg_memory_mb": 320},
    {"name": "Google Drive",   "category": "Work",    "avg_session_duration": 240,  "avg_memory_mb": 110},

    # ── Social ───────────────────────────────────────────────────────────────
    {"name": "Instagram",      "category": "Social",  "avg_session_duration": 900,  "avg_memory_mb": 200},
    {"name": "WhatsApp",       "category": "Social",  "avg_session_duration": 420,  "avg_memory_mb": 130},
    {"name": "Snapchat",       "category": "Social",  "avg_session_duration": 480,  "avg_memory_mb": 210},
    {"name": "Twitter/X",      "category": "Social",  "avg_session_duration": 600,  "avg_memory_mb": 160},
    {"name": "YouTube",        "category": "Social",  "avg_session_duration": 1800, "avg_memory_mb": 280},

    # ── Utility ──────────────────────────────────────────────────────────────
    {"name": "Google Maps",    "category": "Utility", "avg_session_duration": 300,  "avg_memory_mb": 170},
    {"name": "Spotify",        "category": "Utility", "avg_session_duration": 2400, "avg_memory_mb": 140},
    {"name": "Chrome",         "category": "Utility", "avg_session_duration": 600,  "avg_memory_mb": 250},
    {"name": "Calculator",     "category": "Utility", "avg_session_duration": 60,   "avg_memory_mb": 30},
    {"name": "Camera",         "category": "Utility", "avg_session_duration": 120,  "avg_memory_mb": 90},

    # ── Gaming ───────────────────────────────────────────────────────────────
    {"name": "BGMI",           "category": "Gaming",  "avg_session_duration": 2700, "avg_memory_mb": 600},
    {"name": "Candy Crush",    "category": "Gaming",  "avg_session_duration": 600,  "avg_memory_mb": 180},
    {"name": "Chess",          "category": "Gaming",  "avg_session_duration": 900,  "avg_memory_mb": 100},
    {"name": "Subway Surfers", "category": "Gaming",  "avg_session_duration": 480,  "avg_memory_mb": 220},
    {"name": "Amazon",         "category": "Gaming",  "avg_session_duration": 360,  "avg_memory_mb": 150},
    # Note: Amazon is miscategorised as Gaming in the spec — kept as-is.
]

# Quick lookup dict: app name → full record
APP_BY_NAME = {app["name"]: app for app in APP_CATALOG}

# All app names, for convenience
APP_NAMES = [app["name"] for app in APP_CATALOG]
