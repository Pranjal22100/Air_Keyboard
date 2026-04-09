import cv2
import time
from src.config import KEY_WIDTH, KEY_HEIGHT, LARGE_KEYS, KEY_SPACING

class KeyboardUI:
    def __init__(self, start_y=120, start_x=50):
        self.start_y = start_y
        self.start_x = start_x
        self.key_positions = {} # (row_index, key_index) -> (x, y, width)

    def generate_key_positions(self, keyboard):
        positions = []
        y_current = self.start_y
        for row_index, row in enumerate(keyboard):
            x_current = self.start_x
            row_positions = []
            for key in row:
                width = LARGE_KEYS.get(key, KEY_WIDTH)
                row_positions.append((x_current, y_current, width))
                x_current += width + KEY_SPACING
            positions.append(row_positions)
            y_current += KEY_HEIGHT + KEY_SPACING
        return positions

    def draw_keyboard(self, image, keyboard, key_positions, pressed_key, highlight_start_time, caps_lock_on, current_mode, current_buffer, suggestions):
        # Draw Suggestion Bar / Mode Indicator
        cv2.rectangle(image, (50, 20), (1230, 90), (40, 40, 40), -1)
        
        if current_mode == "EN_QWERTY":
            cv2.putText(image, f"Typing: {current_buffer}", (60, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            for i, s_word in enumerate(suggestions):
                sx = 60 + (i * 200)
                cv2.rectangle(image, (sx, 55), (sx + 180, 85), (80, 80, 80), -1)
                display_word = s_word.upper() if caps_lock_on else s_word
                cv2.putText(image, display_word, (sx + 10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        elif current_mode == "HI_PHONETIC":
            cv2.putText(image, "MODE: HINDI PHONETIC (OS IME REQUIRED - Alt+Shift)", (60, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        elif current_mode == "EN_SHORTCUT":
            cv2.putText(image, "MODE: SHORTCUTS ACTIVE", (60, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

        # Draw Keys
        for row_index, row in enumerate(keyboard):
            for key_index, key in enumerate(row):
                x, y, width = key_positions[row_index][key_index]
                color = (0, 0, 0)
                if key == pressed_key and time.time() - highlight_start_time < 0.5:
                    color = (0, 255, 0)
                
                cv2.rectangle(image, (x, y), (x + width, y + KEY_HEIGHT), color, -1)
                cv2.putText(image, key, (x + 10, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.rectangle(image, (x, y), (x + width, y + KEY_HEIGHT), (50, 50, 50), 2)
                
                if key == "Caps" and caps_lock_on and current_mode == "EN_QWERTY":
                    cv2.circle(image, (x + width // 2, y + KEY_HEIGHT - 10), 5, (0, 0, 255), -1)
        
        return image

    def check_key_click(self, x, y, keyboard, key_positions):
        for row_index, row in enumerate(keyboard):
            for key_index, key in enumerate(row):
                kx, ky, kw = key_positions[row_index][key_index]
                if kx < x < kx + kw and ky < y < ky + KEY_HEIGHT:
                    return key
        return None
