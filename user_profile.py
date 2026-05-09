"""
User profile for AURA simulator.
Models a 3rd-year CSE college student's weekly app-usage patterns.
Each slot is a list of (app_name, relative_weight) pairs.
"""

import numpy as np

# ── Time-slot definitions (hour ranges, inclusive) ───────────────────────────
SLOTS = {
    "early_morning": range(5, 7),    # 5–6 am  (wake-up, before class prep)
    "morning":       range(7, 9),    # 7–8 am  (class prep, emails)
    "class_hours":   range(9, 17),   # 9 am–4 pm
    "evening":       range(17, 20),  # 5–7 pm
    "night":         range(20, 24),  # 8 pm–11 pm
}

# ── Weekday usage weights ─────────────────────────────────────────────────────
# Higher weight → more likely to be chosen in that slot
WEEKDAY_PROFILE = {
    "early_morning": [
        ("WhatsApp", 4), ("Chrome", 3), ("Gmail", 2),
    ],
    "morning": [
        ("Gmail", 5), ("Slack", 4), ("Chrome", 4),
        ("WhatsApp", 3), ("Twitter/X", 2),
    ],
    "class_hours": [
        ("Google Meet", 5), ("Microsoft Teams", 4), ("Google Drive", 4),
        ("Chrome", 5), ("Slack", 3), ("Gmail", 3), ("WhatsApp", 2),
    ],
    "evening": [
        ("Instagram", 5), ("YouTube", 5), ("Spotify", 4),
        ("WhatsApp", 4), ("Twitter/X", 3), ("Chrome", 2),
    ],
    "night": [
        ("BGMI", 5), ("YouTube", 4), ("Instagram", 4),
        ("Snapchat", 3), ("Candy Crush", 2), ("Spotify", 2),
    ],
}

# ── Weekend usage weights ─────────────────────────────────────────────────────
WEEKEND_PROFILE = {
    "early_morning": [
        ("WhatsApp", 3), ("Instagram", 3),
    ],
    "morning": [
        ("YouTube", 4), ("Instagram", 4), ("Spotify", 3),
        ("WhatsApp", 3), ("Chrome", 3),
    ],
    "class_hours": [
        ("BGMI", 5), ("Subway Surfers", 4), ("Chess", 3),
        ("YouTube", 4), ("Instagram", 3), ("Snapchat", 3),
    ],
    "evening": [
        ("Instagram", 5), ("YouTube", 5), ("WhatsApp", 4),
        ("Snapchat", 3), ("Twitter/X", 3), ("Spotify", 3),
    ],
    "night": [
        ("BGMI", 6), ("Candy Crush", 3), ("YouTube", 4),
        ("Instagram", 3), ("Snapchat", 3),
    ],
}

# ── Anomaly pool ──────────────────────────────────────────────────────────────
# On anomaly days the student's routine breaks completely
# (e.g. hackathon, exam night, trip, sick day)
ANOMALY_POOL = [
    # Hackathon / project crunch — heavy work + Chrome all day
    [("Chrome", 6), ("Google Meet", 5), ("Slack", 5), ("Google Drive", 4),
     ("Gmail", 3), ("YouTube", 2)],

    # Exam night — no social, heavy studying
    [("Chrome", 6), ("Google Drive", 5), ("Spotify", 4), ("Gmail", 3),
     ("Calculator", 3), ("YouTube", 2)],

    # Social binge / weekend trip — barely any work
    [("Instagram", 6), ("Snapchat", 5), ("WhatsApp", 5),
     ("YouTube", 4), ("Google Maps", 4), ("Camera", 4)],

    # Gaming marathon
    [("BGMI", 8), ("Subway Surfers", 4), ("Chess", 3),
     ("YouTube", 4), ("WhatsApp", 2)],
]


def get_slot_for_hour(hour: int) -> str:
    """Return the time-slot name for a given hour (0–23)."""
    for slot, hours in SLOTS.items():
        if hour in hours:
            return slot
    return None  # midnight–4 am → no slot (user is asleep)


def sample_app(hour: int, day_of_week: int, rng: np.random.Generator,
               is_anomaly: bool = False, anomaly_variant: int = 0) -> str | None:
    """
    Draw a single app open event for the given hour and day.
    Returns None if the user is likely asleep (no slot).
    """
    slot = get_slot_for_hour(hour)
    if slot is None:
        return None  # asleep

    if is_anomaly:
        pool = ANOMALY_POOL[anomaly_variant % len(ANOMALY_POOL)]
    elif day_of_week >= 5:  # Saturday=5, Sunday=6
        pool = WEEKEND_PROFILE[slot]
    else:
        pool = WEEKDAY_PROFILE[slot]

    apps, weights = zip(*pool)
    weights = np.array(weights, dtype=float)
    weights /= weights.sum()
    return rng.choice(apps, p=weights)
