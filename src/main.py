import cv2
import time
from src.config import (
    CAMERA_WIDTH, CAMERA_HEIGHT, THRESHOLD_DISTANCE,
    DEFAULT_KEYBOARD, SHORTCUT_KEYBOARD, HINDI_PHONETIC_KEYBOARD
)
from src.hand_tracker import HandTracker
from src.keyboard_ui import KeyboardUI
from src.input_handler import InputHandler
from src.suggestion_engine import SuggestionEngine

class AirKeyboardApp:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

        self.tracker = HandTracker()
        self.ui = KeyboardUI()
        self.input = InputHandler()
        self.suggestions = SuggestionEngine()

        self.current_keyboard = DEFAULT_KEYBOARD
        self.key_positions = self.ui.generate_key_positions(self.current_keyboard)
        self.current_mode = "EN_QWERTY"
        self.caps_lock_on = False
        self.current_buffer = ""
        self.active_suggestions = []
        
        self.pressed_key = None
        self.highlight_start_time = 0
        self.is_pressed = False

    def run(self):
        while self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                break

            image = cv2.flip(image, 1)
            image = self.tracker.find_hands(image)
            lm_list = self.tracker.get_landmarks(image)

            if lm_list:
                # 4 is thumb tip, 8 is index tip
                length, image, line_info = self.tracker.get_distance(lm_list[4], lm_list[8], image)
                
                if length < THRESHOLD_DISTANCE:
                    if not self.is_pressed:
                        cx, cy = line_info[4], line_info[5]
                        key = self.ui.check_key_click(cx, cy, self.current_keyboard, self.key_positions)
                        if key:
                            self.handle_key_press(key)
                        self.is_pressed = True
                else:
                    self.is_pressed = False

            image = self.ui.draw_keyboard(
                image, self.current_keyboard, self.key_positions,
                self.pressed_key, self.highlight_start_time,
                self.caps_lock_on, self.current_mode,
                self.current_buffer, self.active_suggestions
            )

            cv2.imshow("Air Keyboard", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def handle_key_press(self, key):
        self.pressed_key = key
        self.highlight_start_time = time.time()

        if key == "Switch to Shortcuts":
            self.current_keyboard = SHORTCUT_KEYBOARD
            self.current_mode = "EN_SHORTCUT"
            self.key_positions = self.ui.generate_key_positions(self.current_keyboard)
        elif key == "Switch to Hindi":
            self.input.switch_os_layout()
            self.current_keyboard = HINDI_PHONETIC_KEYBOARD
            self.current_mode = "HI_PHONETIC"
            self.key_positions = self.ui.generate_key_positions(self.current_keyboard)
        elif key in ["Back to QWERTY", "Switch to QWERTY"]:
            if self.current_mode == "HI_PHONETIC":
                self.input.switch_os_layout()
            self.current_keyboard = DEFAULT_KEYBOARD
            self.current_mode = "EN_QWERTY"
            self.current_buffer = ""
            self.key_positions = self.ui.generate_key_positions(self.current_keyboard)
        elif key == "Caps":
            self.caps_lock_on = not self.caps_lock_on
        elif key == "Backspace":
            self.input.press_key("backspace")
            if self.current_mode == "EN_QWERTY":
                self.current_buffer = self.current_buffer[:-1]
                self.active_suggestions = self.suggestions.get_suggestions(self.current_buffer)
        elif key in ["Space", "Enter"]:
            self.input.press_key(key.lower())
            if self.current_mode == "EN_QWERTY":
                self.current_buffer = ""
                self.active_suggestions = []
        else:
            # Check if it's a suggestion click? No, current logic only handles keyboard clicks.
            # Standard typing logic
            char = key.upper() if self.caps_lock_on else key.lower()
            if self.current_mode == "HI_PHONETIC":
                char = key.lower()
            
            self.input.press_key(char)
            
            if self.current_mode == "EN_QWERTY" and len(key) == 1:
                self.current_buffer += char
                self.active_suggestions = self.suggestions.get_suggestions(self.current_buffer)

if __name__ == "__main__":
    app = AirKeyboardApp()
    app.run()
