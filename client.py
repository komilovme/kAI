import keyboard
import pyautogui
import requests
import tempfile
import time
import os
import tkinter as tk
import threading
import win32gui
import win32con


OCR_URL = "https://kai-d0f8.onrender.com/ocr"

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


def analyse_screen():
    show_tooltip("Analysing...", duration=5)

    screenshot = pyautogui.screenshot()

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        screenshot.save(f.name)
        img_path = f.name

    try:
        with open(img_path, "rb") as img:
            response = requests.post(
                OCR_URL,
                files={"file": img}
            )

        data = response.json()
        print("OCR TEXT:\n", data.get("text"))

    finally:
        os.remove(img_path)


def main():
    print("Running in background... Press CTRL + ALT + A")

    keyboard.add_hotkey("ctrl+alt+a", analyse_screen)
    keyboard.wait()

if __name__ == "__main__":
    main()
