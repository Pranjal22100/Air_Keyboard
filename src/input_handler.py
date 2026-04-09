import pyautogui
from playsound import playsound
import os
from src.config import SPECIAL_KEYS_MAP, CLICK_SOUND_PATH

class InputHandler:
    def __init__(self):
        pyautogui.PAUSE = 0.05

    def play_click_sound(self):
        if os.path.exists(CLICK_SOUND_PATH):
            try:
                playsound(CLICK_SOUND_PATH, block=False)
            except Exception as e:
                print(f"Error playing sound: {e}")

    def press_key(self, key):
        if key.lower() == "print screen":
            pyautogui.hotkey("printscreen")
        elif key in SPECIAL_KEYS_MAP:
            pyautogui.press(SPECIAL_KEYS_MAP[key])
        elif "+" in key:
            keys = key.split("+")
            pyautogui.hotkey(*[k.lower() for k in keys])
        else:
            pyautogui.typewrite(key)
        
        self.play_click_sound()

    def switch_os_layout(self):
        pyautogui.hotkey('alt', 'shift')
