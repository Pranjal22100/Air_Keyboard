import cv2
import mediapipe as mp
import math
import time
import pyautogui
from playsound import playsound
import wordfreq 

# --- INITIALIZATION ---

# Initialize MediaPipe Hands and Drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# --- WORD COMPLETION SETUP ---
current_typing_buffer = ""  # Tracks the current word being typed (English only)
suggestions = []

# Threshold distance for "click"
THRESHOLD_DISTANCE = 30

# Increase camera resolution
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Sound file for click feedback
CLICK_SOUND = "click_sound.mp3"

# --- KEYBOARD LAYOUTS ---
# 1. English QWERTY Layout
default_keyboard = [
    ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "<", ">","{"],
    ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "?", '"',"}"],
    ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", ":", "Backspace"],
    ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
    ["Caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
    ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift", "Up"],
    ["Ctrl", "Win", "Alt", "Space", "Alt", "Fn", "Ctrl", "Left", "Down", "Right"],
    ["Switch to Shortcuts", "Switch to Hindi"] # New row for mode switching
]

# 2. Shortcut Layout
shortcut_keyboard = [
    ["Ctrl+C", "Ctrl+V", "Ctrl+X", "Ctrl+Z", "Ctrl+Y"],
    ["Alt+Tab", "Alt+F4", "Win+D"],
    ["Print Screen", "Shift+Del", "Ctrl+Shift+T", "Ctrl+T", "Shift+Enter"],
    ["Back to QWERTY"] # Button to exit shortcut mode
]

# 3. Hindi Phonetic Layout (Same keys as QWERTY)
hindi_phonetic_keyboard = [
    ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "<", ">","{"],
    ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "?", '"',"}"],
    ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", ":", "Backspace"],
    ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
    ["Caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
    ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift", "Up"],
    ["Ctrl", "Win", "Alt", "Space", "Alt", "Fn", "Ctrl", "Left", "Down", "Right"],
    ["Switch to QWERTY"] # Button to exit Hindi mode
]

# --- STATE MANAGEMENT ---
current_keyboard = default_keyboard
caps_lock_on = False
KEY_WIDTH, KEY_HEIGHT = 60, 60
# Tracks the current operating mode: "EN_QWERTY", "EN_SHORTCUT", or "HI_PHONETIC"
current_mode = "EN_QWERTY" 

# Large key adjustments 
LARGE_KEYS = {
    "Backspace": 130, "Tab": 90, "Caps": 105, "Enter": 145, "Shift": 135,
    "Space": 490, 
    "Switch to Shortcuts": 150, "Switch to Hindi": 150, "Back to QWERTY": 150, "Switch to QWERTY": 150,
    "Ctrl+C": 140, "Ctrl+V": 140, "Ctrl+X": 140, "Ctrl+Z": 140, "Ctrl+Y": 140,
    "Alt+Tab": 140, "Alt+F4": 140, "Win+D": 140, "Print Screen": 140, "Shift+Del": 140, 
    "Ctrl+Shift+T": 180, "Ctrl+T": 140, "Shift+Enter": 180
}

# Function to generate key positions
def generate_key_positions(keyboard):
    positions = []
    y_start = 120 
    for row_index, row in enumerate(keyboard):
        x_start = 50
        row_positions = []
        for key in row:
            width = LARGE_KEYS.get(key, KEY_WIDTH)
            row_positions.append((x_start, y_start + row_index * (KEY_HEIGHT + 10), width))
            x_start += width + 10
        positions.append(row_positions)
    return positions

key_positions = generate_key_positions(current_keyboard)

SPECIAL_KEYS = {
    "Backspace": "backspace", "Enter": "enter", "Space": "space", "Tab": "tab",
    "Shift": "shift", "Ctrl": "ctrl", "Alt": "alt", "Caps": "capslock",
    "Esc": "esc", "Win": "win", "Up": "up", "Down": "down", "Left": "left",
    "Right": "right", "F1": "f1", "F2": "f2", "F3": "f3", "F4": "f4", "F5": "f5",
    "F6": "f6", "F7": "f7", "F8": "f8", "F9": "f9", "F10": "f10", "F11": "f11", "F12": "f12"
}

# Function to update suggestions (English only)
def update_suggestions():
    global suggestions, current_typing_buffer
    if len(current_typing_buffer) < 2:
        suggestions = []
        return
    
    prefix = current_typing_buffer.lower()
    
    # Get a large list of the most frequent English words
    frequent_words = wordfreq.top_n_list(lang='en', n=50000, wordlist='best')
    
    # Manually filter the frequent words list based on the current prefix
    matches = []
    for word in frequent_words:
        if word.startswith(prefix):
            matches.append(word)
        
        # Stop after finding enough highly relevant words
        if len(matches) >= 5:
            break
            
    suggestions = matches

# Function to handle key presses and state changes
def press_key(key):
    global caps_lock_on, current_typing_buffer, current_mode, current_keyboard, key_positions
    
    # --- CYCLING SWITCH LOGIC (UPDATED) ---
    
    if key == "Switch to Shortcuts":
        current_keyboard = shortcut_keyboard
        current_mode = "EN_SHORTCUT"
    
    elif key == "Switch to Hindi":
        # 1. Simulate the OS keyboard layout switch shortcut (Alt+Shift)
        # This assumes your OS switches to Hindi Phonetic layout when this combo is pressed.
        pyautogui.hotkey('alt', 'shift') 
        
        # 2. Switch the virtual keyboard display
        current_keyboard = hindi_phonetic_keyboard
        current_mode = "HI_PHONETIC"
        
    elif key == "Back to QWERTY" or key == "Switch to QWERTY":
        # When switching back to English, simulate the OS switch again (Alt+Shift)
        if current_mode == "HI_PHONETIC":
             pyautogui.hotkey('alt', 'shift') # Cycles back to your primary OS language
             
        current_keyboard = default_keyboard
        current_mode = "EN_QWERTY"
        current_typing_buffer = "" # Clear buffer for English word prediction
        

    # Recalculate positions if the keyboard was switched
    if key in ["Switch to Shortcuts", "Switch to Hindi", "Back to QWERTY", "Switch to QWERTY"]:
        key_positions = generate_key_positions(current_keyboard)
        return

    # --- SPECIAL KEY HANDLING ---
    if key.lower() == "print screen":
        pyautogui.hotkey("printscreen")
    elif key == "Caps":
        caps_lock_on = not caps_lock_on
    elif key == "Backspace":
        pyautogui.press("backspace")
        if current_mode == "EN_QWERTY":
             current_typing_buffer = current_typing_buffer[:-1]
    elif key in ["Space", "Enter"]:
        pyautogui.press(SPECIAL_KEYS[key])
        if current_mode == "EN_QWERTY":
            current_typing_buffer = ""
    elif key in SPECIAL_KEYS and SPECIAL_KEYS[key]:
        pyautogui.press(SPECIAL_KEYS[key])
    elif "+" in key:
        keys = key.split("+")
        pyautogui.hotkey(*[k.lower() for k in keys])

    # --- STANDARD CHARACTER TYPING LOGIC ---
    else: # This block handles all standard keys (A-Z, 1-0, symbols)
        
        if current_mode == "EN_QWERTY":
            # English Mode: Respect Caps Lock and track buffer
            char = key.upper() if caps_lock_on else key.lower()
            pyautogui.typewrite(char)
            
            if len(key) == 1:
                current_typing_buffer += char
                update_suggestions() 
                
        elif current_mode == "HI_PHONETIC":
            # Hindi Phonetic Mode: Always send lowercase Roman character
            char = key.lower() 
            pyautogui.typewrite(char)


# Function to draw the keyboard 
def draw_keyboard(image):
    global pressed_key, highlight_start_time
    
    # --- Draw Suggestion Bar / Mode Indicator ---
    cv2.rectangle(image, (50, 20), (1230, 90), (40, 40, 40), -1)
    
    if current_mode == "EN_QWERTY":
        # Show buffer and suggestions in English mode
        cv2.putText(image, f"Typing: {current_typing_buffer}", (60, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        for i, s_word in enumerate(suggestions):
            sx = 60 + (i * 200)
            cv2.rectangle(image, (sx, 55), (sx + 180, 85), (80, 80, 80), -1)
            display_word = s_word.upper() if caps_lock_on else s_word
            cv2.putText(image, display_word, (sx + 10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    elif current_mode == "HI_PHONETIC":
        # Show Hindi mode status
        cv2.putText(image, "MODE: HINDI PHONETIC (OS IME REQUIRED - Alt+Shift PRESSED)", (60, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    elif current_mode == "EN_SHORTCUT":
        # Show Shortcut mode status
        cv2.putText(image, "MODE: SHORTCUTS ACTIVE", (60, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)


    # Draw Keyboard Keys 
    for row_index, row in enumerate(current_keyboard):
        for key_index, key in enumerate(row):
            x, y, width = key_positions[row_index][key_index]
            color = (0, 0, 0)
            if key == pressed_key and time.time() - highlight_start_time < 1:
                color = (0, 255, 0)
            cv2.rectangle(image, (x, y), (x + width, y + KEY_HEIGHT), color, -1)
            cv2.putText(image, key, (x + 10, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.rectangle(image, (x, y), (x + width, y + KEY_HEIGHT), (50, 50, 50), 2)
            if key == "Caps" and caps_lock_on and current_mode == "EN_QWERTY":
                cv2.circle(image, (x + width // 2, y + KEY_HEIGHT - 10), 5, (0, 0, 255), -1)

# Initialize variables
pressed_key = None
highlight_start_time = 0
is_pressed = False

# Main loop
with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success: continue

        image = cv2.flip(image, 1)
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw_keyboard(image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                h, w, _ = image.shape
                ix, iy = int(index_tip.x * w), int(index_tip.y * h)
                tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)
                distance = math.hypot(ix - tx, iy - ty)

                if distance < THRESHOLD_DISTANCE and not is_pressed:
                    suggestion_clicked = False
                    
                    # --- CHECK FOR SUGGESTION CLICK (ONLY IN EN_QWERTY MODE) ---
                    if current_mode == "EN_QWERTY" and 55 <= iy <= 85:
                        for i, suggested_word in enumerate(suggestions):
                            sx = 60 + (i * 200)
                            if sx <= ix <= sx + 180:
                                # 1. Delete the current partial word
                                for _ in range(len(current_typing_buffer)):
                                    pyautogui.press('backspace')
                                
                                # 2. Determine capitalization
                                final_word = suggested_word.upper() if caps_lock_on else suggested_word
                                
                                # 3. Type the suggested word + a space
                                pyautogui.typewrite(final_word + " ")
                                current_typing_buffer = ""
                                suggestions = [] # Clear suggestions
                                is_pressed = True
                                suggestion_clicked = True
                                playsound(CLICK_SOUND, block=False)
                                break
                    
                    # --- CHECK FOR KEYBOARD CLICK ---
                    if not suggestion_clicked:
                        for row_index, row in enumerate(current_keyboard):
                            for key_index, key in enumerate(row):
                                x, y, width = key_positions[row_index][key_index]
                                if x <= ix <= x + width and y <= iy <= y + KEY_HEIGHT:
                                    pressed_key = key
                                    highlight_start_time = time.time()
                                    is_pressed = True
                                    playsound(CLICK_SOUND, block=False)
                                    
                                    # Call press_key to handle the key logic, including mode switching
                                    press_key(key)
                                    break
                elif distance >= THRESHOLD_DISTANCE:
                    is_pressed = False

        cv2.imshow("Virtual Keyboard", image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()