# Air Keyboard

![Project: Air Keyboard](https://img.shields.io/badge/Air%20Keyboard-experimental-orange)
![Status](https://img.shields.io/badge/status-in--progress-red)
![License](https://img.shields.io/badge/license-ISC-lightgrey)

> ⚠️ **Status:** This project is currently under active development. Features may change, and stability is not guaranteed. Contributions and feedback are welcome!


## Table of Contents

- [What the project does](#what-the-project-does)
- [Why the project is useful](#why-the-project-is-useful)
- [Key features](#key-features)
- [Architecture](#architecture)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Quick start](#quick-start)
- [Usage guide](#usage-guide)
  - [Hand gestures](#hand-gestures)
  - [Keyboard layouts](#keyboard-layouts)
  - [Word suggestions](#word-suggestions)
- [Configuration](#configuration)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Who maintains this project](#who-maintains-this-project)

## What the project does

**Air Keyboard** is a gesture-based virtual keyboard written in Python that uses hand gesture recognition to emulate system keyboard input. Point your camera at your hands, pinch your thumb and index finger to "click" on virtual keys displayed on screen, and your computer registers the input.

Supports three keyboard layouts: English QWERTY (with word suggestions), keyboard shortcuts (Ctrl+C, Alt+Tab, etc.), and Hindi Phonetic input via OS IME integration.

## Why the project is useful

- **Hands-free input** — No physical keyboard needed; any camera device works
- **Modern, accessible** — Useful for touchless environments or accessibility needs
- **Multi-language support** — Switch between English and Hindi layouts
- **Smart suggestions** — Auto-completion for English words based on frequency
- **Shortcut mode** — Quick access to common keyboard shortcuts
- **Visual feedback** — Highlighted key presses and audio clicks
- **Real-time processing** — Low-latency gesture recognition with MediaPipe
- **Integration-ready** — Works with any application via OS keyboard simulation

## Key features

- Real-time hand gesture detection (thumb-to-index pinch = click)
- Three keyboard layouts: QWERTY, Shortcuts, Hindi Phonetic
- English word suggestions with caps-lock awareness
- Audio feedback on key press
- Multi-hand support (up to 2 hands simultaneously)
- Adjustable click threshold and keyboard sensitivity
- Caps Lock toggle with visual indicator
- Special keys: Function keys, arrow keys, shortcuts, modifiers
- OS keyboard layout switching (Alt+Shift for Hindi IME)

## Architecture

- **Core**: `Air_Keyboard.py` (Main runner script)
- **Source Code**: `src/`
  - `main.py`: Application entry point and main loop.
  - `hand_tracker.py`: Handles MediaPipe hand landmark detection and distance calculation.
  - `keyboard_ui.py`: Manages OpenCV-based virtual keyboard rendering and layout logic.
  - `input_handler.py`: Interface for OS keyboard simulation and audio feedback.
  - `suggestion_engine.py`: Logic for English word predictions using frequency data.
  - `config.py`: Global constants, keyboard layouts, and configuration settings.
- **Assets**: `assets/` (For sounds and other static files)
- **Dependencies**: `requirements.txt`
- **Git**: `.gitignore` (Standard Python project exclusions)

No backend, no frontend—modular Python application.

## Getting started

### Prerequisites

- Python 3.8+ (64-bit)
- Webcam or external camera
- Windows, macOS, or Linux
- ~2 GiB disk space for dependencies

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Air_Keyboard.git
cd Air_Keyboard

# Install dependencies
pip install opencv-python mediapipe pyautogui playsound wordfreq
```

**Optional:** Add click sound file:

```bash
# Place an MP3 file in the project root
# File path: Air_Keyboard/click_sound.mp3
```

### Quick start

```bash
# Run the application
python Air_Keyboard.py
```

A window will open showing:
- Live webcam feed with hand landmarks
- Virtual keyboard overlay
- Current typing buffer and suggestions (English mode)

## Usage guide

### Hand gestures

1. **Click a key** — Pinch thumb and index finger together. When distance < threshold (~30 pixels), the key is activated.
2. **Release** — Separate thumb and index finger to release.
3. **Multi-hand** — Use both hands simultaneously for different inputs.

### Keyboard layouts

**English QWERTY Mode** (default)
- Full QWERTY layout with numbers, symbols, function keys
- Word suggestions appear in the top bar
- Caps Lock can be toggled; shows red indicator
- Special keys: Backspace, Enter, Shift, Ctrl, Alt, Space

**Shortcuts Mode**
- Common Windows/Linux shortcuts: Ctrl+C, Ctrl+V, Alt+Tab, Ctrl+Z, etc.
- Access via "Switch to Shortcuts" button
- Return to QWERTY with "Back to QWERTY" button

**Hindi Phonetic Mode**
- Same QWERTY layout; OS handles transliteration to Devanagari
- Requires Hindi IME installed and configured on your OS
- System hotkey (Alt+Shift) is auto-triggered during switch
- Return to English with "Switch to QWERTY" button

### Word suggestions

**English mode only:**
1. Start typing a word (e.g., "hel")
2. Top bar shows suggestions: "hello", "help", "helicopter", etc. (top 5)
3. Pinch near a suggestion to insert it + space
4. Buffer clears after space or Enter

> Suggestions use `wordfreq` library (top 50K English words by frequency).

## Configuration

Edit `Air_Keyboard.py` to customize:

```python
# Threshold distance for click detection (lower = stricter pinch)
THRESHOLD_DISTANCE = 30  # pixels

# Webcam resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Key dimensions
KEY_WIDTH, KEY_HEIGHT = 60, 60

# Click sound file
CLICK_SOUND = "click_sound.mp3"

# Hand detection confidence
min_detection_confidence=0.7, min_tracking_confidence=0.7
```

## Screenshots

- ![Main keyboard view](docs/screenshots/keyboard-main.png)
- ![English mode with suggestions](docs/screenshots/english-suggestions.png)
- ![Shortcuts mode](docs/screenshots/shortcuts-mode.png)
- ![Hand gesture detection](docs/screenshots/hand-detection.png)

## Troubleshooting

### Hand not detected
- Ensure good lighting (backlighting helps)
- Move closer to camera
- Increase `min_detection_confidence` threshold in code
- Calibrate webcam orientation

### Keys not registering
- Pinch thumb and index finger more firmly
- Reduce `THRESHOLD_DISTANCE` value
- Ensure webcam has enough FPS (15+ recommended)

### Word suggestions not appearing
- Verify `wordfreq` library is installed: `pip install wordfreq`
- Check that you're in English QWERTY mode
- Buffer must have at least 2+ characters

### Click sound not playing
- Verify `click_sound.mp3` exists in project root
- Try different audio format (WAV instead of MP3)
- For silent mode, comment out `playsound()` lines

### Hindi mode not working
- Verify Hindi IME is installed on your OS (Settings > Language & Region)
- Set Hindi Phonetic as input method
- Test Alt+Shift keyboard shortcut manually first
- May require OS-specific setup (varies by Windows/Linux/macOS)

## Who maintains this project

Maintainer: [Pranjal Verma].

> Personal project for resume/portfolio purposes. Explore gesture recognition, computer vision, and OS interaction in Python.

### Project Status

- ✅ Hand gesture detection and click mechanism working
- ✅ English QWERTY layout with word suggestions
- ✅ Keyboard shortcuts mode
- 🔄 Hindi Phonetic mode (requires OS-level testing)
- 🔄 Performance optimization for real-time detection
- 📋 Additional features planned (mouse control, custom layouts, settings UI)

> **Note:** This project is actively under development. Core functionality is stable, but some features are being refined. Check the [GitHub Issues](docs/issues) for known limitations and planned improvements.

---

> Proof-of-concept for hand gesture recognition. For production touchless input systems, consider integrating with accessibility APIs or dedicated hardware sensors.
