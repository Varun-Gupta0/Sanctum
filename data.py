# Small house layout data - Structural Graph

rooms = [
    {"id": "room_1", "name": "Living Room",   "width": 15, "length": 18, "x": 0,  "y": 0},
    {"id": "room_2", "name": "Kitchen",       "width": 12, "length": 14, "x": 15, "y": 0},
    {"id": "room_3", "name": "Master Bedroom","width": 14, "length": 16, "x": 0,  "y": 18},
    {"id": "room_4", "name": "Bedroom 2",     "width": 12, "length": 12, "x": 14, "y": 18},
    {"id": "room_5", "name": "Bathroom",      "width": 8,  "length": 10, "x": 14, "y": 30},
    {"id": "room_6", "name": "Hallway",       "width": 4,  "length": 12, "x": 27, "y": 0},
]

walls = [
    {"id": "w1", "type": "load_bearing", "length": 34, "x1": 0, "y1": 0, "x2": 0, "y2": 34, "room_id": "room_1"},
    {"id": "w2", "type": "load_bearing", "length": 31, "x1": 0, "y1": 0, "x2": 31, "y2": 0, "room_id": "room_1"},
    {"id": "w3", "type": "load_bearing", "length": 12, "x1": 31, "y1": 0, "x2": 31, "y2": 12, "room_id": "room_6"},
    {"id": "w4", "type": "load_bearing", "length": 22, "x1": 0, "y1": 34, "x2": 22, "y2": 34, "room_id": "room_3"},
    {"id": "w5", "type": "partition",    "length": 14, "x1": 15, "y1": 0, "x2": 15, "y2": 14, "room_id": "room_2"},
    {"id": "w6", "type": "partition",    "length": 15, "x1": 0, "y1": 18, "x2": 15, "y2": 18, "room_id": "room_1"},
    {"id": "w7", "type": "partition",    "length": 16, "x1": 14, "y1": 18, "x2": 14, "y2": 34, "room_id": "room_3"},
    {"id": "w8", "type": "partition",    "length": 12, "x1": 15, "y1": 14, "x2": 27, "y2": 14, "room_id": "room_2"},
]
