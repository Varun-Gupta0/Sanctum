# Small house layout data

rooms = [
    {"name": "Living Room",   "width": 15, "length": 18, "x": 0,  "y": 0},
    {"name": "Kitchen",       "width": 12, "length": 14, "x": 15, "y": 0},
    {"name": "Master Bedroom","width": 14, "length": 16, "x": 0,  "y": 18},
    {"name": "Bedroom 2",     "width": 12, "length": 12, "x": 14, "y": 18},
    {"name": "Bathroom",      "width": 8,  "length": 10, "x": 14, "y": 30},
    {"name": "Hallway",       "width": 4,  "length": 12, "x": 27, "y": 0},
]

walls = [
    {"type": "load_bearing", "length": 31},
    {"type": "load_bearing", "length": 27},
    {"type": "load_bearing", "length": 40},
    {"type": "load_bearing", "length": 27},
    {"type": "partition",    "length": 18},
    {"type": "partition",    "length": 14},
    {"type": "partition",    "length": 12},
    {"type": "partition",    "length": 10},
]
