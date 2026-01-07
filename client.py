import keyboard
import pyautogui
import requests
import tempfile
import os
import tkinter as tk
import threading
import win32gui
import win32con
import base64
from io import BytesIO

# === SERVER URLS ===
OCR_URL = "https://kai-d0f8.onrender.com/ocr"
AI_URL  = "https://kai-1-c89l.onrender.com/ai"
AI_IMAGE_URL = "https://kai-1-c89l.onrender.com/ai-image"


# === TOOLTIP ===
def show_tooltip(text="Analysing...", duration=3):
    def _tooltip():
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.attributes("-alpha", 0.9)

        x, y = pyautogui.position()
        root.geometry(f"+{x+15}+{y+15}")

        label = tk.Label(
            root,
            text=text,
            bg="#1e1e1e",
            fg="white",
            font=("Segoe UI", 9),
            padx=8,
            pady=4
        )
        label.pack()

        hwnd = win32gui.GetParent(root.winfo_id())
        win32gui.SetWindowLong(
            hwnd,
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            | win32con.WS_EX_TOOLWINDOW
        )

        root.after(duration * 1000, root.destroy)
        root.mainloop()

    threading.Thread(target=_tooltip, daemon=True).start()


# === MAIN LOGIC ===
def analyse_screen():
    show_tooltip("Analysing...", duration=5)

    screenshot = pyautogui.screenshot()

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        screenshot.save(f.name)
        img_path = f.name

    try:
        # 1️⃣ OCR REQUEST
        with open(img_path, "rb") as img:
            ocr_res = requests.post(
                OCR_URL,
                files={"file": img},
                timeout=30
            )

        ocr_data = ocr_res.json()
        text = ocr_data.get("text", "").strip()

        # print("OCR TEXT:\n", text)

        if not text:
            show_tooltip("No text detected", duration=3)
            return

        # 2️⃣ AI REQUEST
        ai_res = requests.post(
            AI_URL,
            json={"text": text},
            timeout=30
        )

        ai_data = ai_res.json()
        print("AI RESPONSE:\n", ai_data)

        answer = ai_data.get("answer", "Done")

        # 3️⃣ SHOW ANSWER (STEALTH)
        show_tooltip(answer, duration = 10)

    except Exception as e:
        print("ERROR:", e)
        show_tooltip("Error", duration=3)

    finally:
        os.remove(img_path)

def screenshot_to_base64():
    img = pyautogui.screenshot()
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def analyse_image():
    show_tooltip("Analysing image...", duration=5)

    try:
        img_b64 = screenshot_to_base64()

        res = requests.post(
            AI_IMAGE_URL,
            json={"image_base64": img_b64},
            timeout=40
        )

        data = res.json()
        print("AI IMAGE RESPONSE:", data)

        answer = data.get("answer", "Done")
        show_tooltip(answer, duration=4)

    except Exception as e:
        print("IMAGE ERROR:", e)
        show_tooltip("Image error", duration=3)


# === HOTKEY ===
def main():
    print("Running in background...")
    print("CTRL + ALT + A  → OCR + AI")
    print("CTRL + ALT + S  → IMAGE AI")

    keyboard.add_hotkey("ctrl+alt+a", analyse_screen)  # oldingi OCR
    keyboard.add_hotkey("ctrl+alt+s", analyse_image)   # yangi IMAGE
    keyboard.wait()



if __name__ == "__main__":
    main()
