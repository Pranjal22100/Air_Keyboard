import cv2

# --- THRESHOLDS & SETTINGS ---
THRESHOLD_DISTANCE = 30
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CLICK_SOUND_PATH = "assets/click_sound.mp3"

# --- KEYBOARD DIMENSIONS ---
KEY_WIDTH = 60
KEY_HEIGHT = 60
KEY_SPACING = 10

# --- KEYBOARD LAYOUTS ---
DEFAULT_KEYBOARD = [
    ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "<", ">","{"],
    ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "?", '"',"}"],
    ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", ":", "Backspace"],
    ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
    ["Caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
    ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift", "Up"],
    ["Ctrl", "Win", "Alt", "Space", "Alt", "Fn", "Ctrl", "Left", "Down", "Right"],
    ["Switch to Shortcuts", "Switch to Hindi"]
]

SHORTCUT_KEYBOARD = [
    ["Ctrl+C", "Ctrl+V", "Ctrl+X", "Ctrl+Z", "Ctrl+Y"],
    ["Alt+Tab", "Alt+F4", "Win+D"],
    ["Print Screen", "Shift+Del", "Ctrl+Shift+T", "Ctrl+T", "Shift+Enter"],
    ["Back to QWERTY"]
]

HINDI_PHONETIC_KEYBOARD = [
    ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "<", ">","{"],
    ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "?", '"',"}"],
    ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", ":", "Backspace"],
    ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
    ["Caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
    ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift", "Up"],
    ["Ctrl", "Win", "Alt", "Space", "Alt", "Fn", "Ctrl", "Left", "Down", "Right"],
    ["Switch to QWERTY"]
]

LARGE_KEYS = {
    "Backspace": 130, "Tab": 90, "Caps": 105, "Enter": 145, "Shift": 135,
    "Space": 490, 
    "Switch to Shortcuts": 150, "Switch to Hindi": 150, "Back to QWERTY": 150, "Switch to QWERTY": 150,
    "Ctrl+C": 140, "Ctrl+V": 140, "Ctrl+X": 140, "Ctrl+Z": 140, "Ctrl+Y": 140,
    "Alt+Tab": 140, "Alt+F4": 140, "Win+D": 140, "Print Screen": 140, "Shift+Del": 140, 
    "Ctrl+Shift+T": 180, "Ctrl+T": 140, "Shift+Enter": 180
}

SPECIAL_KEYS_MAP = {
    "Backspace": "backspace", "Enter": "enter", "Space": "space", "Tab": "tab",
    "Shift": "shift", "Ctrl": "ctrl", "Alt": "alt", "Caps": "capslock",
    "Esc": "esc", "Win": "win", "Up": "up", "Down": "down", "Left": "left",
    "Right": "right", "F1": "f1", "F2": "f2", "F3": "f3", "F4": "f4", "F5": "f5",
    "F6": "f6", "F7": "f7", "F8": "f8", "F9": "f9", "F10": "f10", "F11": "f11", "F12": "f12"
}
