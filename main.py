import os
import sys
import time
import random
import threading
import queue
import tkinter as tk
from utils.browser_manager import BrowserManager
from Codes.WebHandler import WebHandler
import math
from tkinter import messagebox

# ─── Paths & Config
ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
BG = "#07091a"
SURFACE = "#0c0f2e"
PURPLE = "#6c5ce7"
PURPLE_H = "#7d70ef"
TEAL = "#2dd4bf"
TEAL_H = "#3de8d3"
BORDER = "#1a1e45"
TEXT = "#ffffff"
SUBTEXT = "#8892b0"
GOLD = "#f0c060"



# ─── Helpers
def set_icon(root):
    try:
        if os.path.exists(ICON_PATH):
            root.iconbitmap(ICON_PATH)
    except Exception:
        pass


def center(root, w, h):
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")


def draw_stars(canvas, w, h):
    bright = ["#ffffff", "#c8d0ff", "#aabbff"]
    dim = ["#1a1e3a", "#161a38", "#0f1228"]
    for _ in range(110):
        x = random.randint(0, w)
        y = random.randint(0, h)
        r = random.uniform(0.8, 1.5) if random.random() < 0.15 else random.uniform(0.3, 0.9)
        c = random.choice(bright) if random.random() < 0.15 else random.choice(dim)
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=c, outline="")

    # Cosmic gradients (kept as per your original)
    for i in range(12, 0, -1):
        v = i * 5
        color = f"#{min(v, 60):02x}{min(v // 3, 20):02x}{min(v * 3, 180):02x}"
        canvas.create_oval(w - 100 + i * 5, -50 + i * 4, w + 50 - i * 5, 80 - i * 4, fill=color, outline="")
    for i in range(10, 0, -1):
        v = i * 4
        color = f"#{0:02x}{min(v * 2, 100):02x}{min(v * 3, 160):02x}"
        canvas.create_oval(-60 + i * 4, h - 70 + i * 4, 60 - i * 4, h + 50 - i * 4, fill=color, outline="")


def separator(parent, width=260, color=BORDER):
    tk.Frame(parent, bg=color, height=1, width=width).pack(pady=14)


# ─── 1. ICON BUTTON (Animated + Uniform Background)
def styled_btn(parent, text, command, bg=PURPLE, hover_bg=PURPLE_H, fg=TEXT, icon_path=None, width=26, pady_inner=10):
    btn = tk.Button(parent, text=text, command=command, bg=bg, fg=fg, activebackground=hover_bg,
                    activeforeground=fg, font=("Segoe UI", 11, "bold"), relief="flat", bd=0, width=width,
                    pady=pady_inner, cursor="hand2")

    if icon_path and os.path.exists(icon_path):
        img = tk.PhotoImage(file=icon_path)
        btn.config(image=img, compound="left", padx=10)
        btn.image = img  # Keep reference to prevent GC

    # Smooth hover animation
    def on_enter(e): btn.config(bg=hover_bg)

    def on_leave(e): btn.config(bg=bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


# ─── 2. BROWSER CHOICE
def get_browser_choice():
    root = tk.Tk()
    root.title("CUST Portal Reworked")
    root.resizable(False, False)
    root.configure(bg=BG, bd=0, highlightthickness=0)
    set_icon(root)
    W, H = 440, 340
    center(root, W, H)

    canvas = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    draw_stars(canvas, W, H)

    frame = tk.Frame(canvas, bg=BG)
    canvas.create_window(W // 2, H // 2, window=frame, anchor="center")

    choice = {"value": None}

    def select(browser):
        choice["value"] = browser.strip()
        root.destroy()

    tk.Label(frame, text="CUST PORTAL", font=("Segoe UI", 26, "bold"), bg=BG, fg=TEXT).pack()
    tk.Label(frame, text="REWORKED", font=("Segoe UI", 14, "bold"), bg=BG, fg=PURPLE).pack()
    separator(frame)
    tk.Label(frame, text="Select your browser to begin", font=("Segoe UI", 10), bg=BG, fg=SUBTEXT).pack(pady=(0, 16))

    # Replace with your actual icon paths
    chrome_icon = os.path.join("assets", "chrome.png")
    edge_icon = os.path.join("assets", "edge.png")

    styled_btn(frame, "🌐   Microsoft Edge", lambda: select("edge"), icon_path=chrome_icon, bg=PURPLE,
               hover_bg=PURPLE_H).pack(pady=5, ipadx=10)

    root.mainloop()
    return choice["value"]


# ─── 3. WARNING BOX (Fixed White Border + Matches First Box)
def show_warning(browser_name):
    root = tk.Tk()

    root.title("CUST Portal Reworked")
    root.resizable(False, False)
    root.configure(bg=BG)

    set_icon(root)

    W, H = 440, 340
    center(root, W, H)

    canvas = tk.Canvas(
        root,
        width=W,
        height=H,
        bg=BG,
        highlightthickness=0
    )

    canvas.pack(fill="both", expand=True)

    draw_stars(canvas, W, H)

    frame = tk.Frame(canvas, bg=BG)
    canvas.create_window(W//2, H//2, window=frame)

    tk.Label(
        frame,
        text="⚠",
        font=("Segoe UI Emoji", 34),
        bg=BG,
        fg=GOLD
    ).pack(pady=(0, 4))

    tk.Label(
        frame,
        text="CLOSE EDGE",
        font=("Segoe UI", 22, "bold"),
        bg=BG,
        fg=TEXT
    ).pack()

    separator(frame)

    tk.Label(
        frame,
        text=f"Close all active {browser_name.capitalize()} tabs before \nlaunching the scraper.",
        font=("Segoe UI", 10),
        bg=BG,
        fg=SUBTEXT,
        justify="center"
    ).pack(pady=(0, 16))

    warnings = [
        "Existing sessions can break login flow",
        "Portal may attach to wrong browser tab",
        "Scraping may fail unexpectedly"
    ]

    for w in warnings:
        tk.Label(
            frame,
            text=f"• {w}",
            font=("Segoe UI", 9),
            bg=BG,
            fg="#aab4d6"
        ).pack(anchor="w", padx=20, pady=2)

    styled_btn(
        frame,
        "🚀 Continue",
        root.destroy,
        bg=TEAL,
        hover_bg=TEAL_H,
        fg="#071018",
        width=24
    ).pack(pady=(20, 30))

    root.mainloop()


# ─── 4. LOADER OVERLAY (Animated + Thread-Safe)
class LoaderOverlay(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("CUST Portal Reworked")
        self.configure(bg=BG)

        self.resizable(False, False)

        set_icon(self)

        W, H = 440, 340
        center(self, W, H)

        self.canvas = tk.Canvas(
            self,
            width=W,
            height=H,
            bg=BG,
            highlightthickness=0
        )

        self.canvas.pack(fill="both", expand=True)

        draw_stars(self.canvas, W, H)

        self.frame = tk.Frame(self.canvas, bg=BG)

        self.canvas.create_window(
            W//2,
            H//2,
            window=self.frame
        )

        tk.Label(
            self.frame,
            text="Installing Requirements",
            font=("Segoe UI", 22, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=(0, 22))

        self.spinner = tk.Canvas(
            self.frame,
            width=90,
            height=90,
            bg=BG,
            highlightthickness=0
        )

        self.spinner.pack()

        self.status = tk.Label(
            self.frame,
            text="Setting up browser driver",
            font=("Segoe UI", 10),
            bg=BG,
            fg=SUBTEXT
        )

        self.status.pack(pady=(18, 0))

        self.angle = 0
        self.running = True

        self.animate()

    def animate(self):

        if not self.running:
            return

        self.spinner.delete("all")

        for i in range(12):

            angle = math.radians((self.angle + i * 30))

            x = 45 + 24 * math.cos(angle)
            y = 45 + 24 * math.sin(angle)

            size = 3 + (i / 5)

            color = PURPLE if i > 4 else "#2a245e"

            self.spinner.create_oval(
                x-size,
                y-size,
                x+size,
                y+size,
                fill=color,
                outline=""
            )

        self.angle += 6

        dots = "." * ((self.angle // 10) % 1)

        self.status.config(
            text=f"Good Things take time {dots}"
        )

        self.after(40, self.animate)

    def close(self):
        self.running = False
        self.destroy()


# ─── 5. MAIN FLOW (Async Driver + Loader)
def start_bot(driver, browser_choice):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"✅ Selected: {browser_choice.capitalize()}")
    print("⏳ Initializing Flask server...\n")

    handler = WebHandler(data_folder="StudentData", driver=driver)

    def run_flask():
        handler.run(debug=False, host="127.0.0.1", port=5000)

    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(2)
    print("✅ Flask running at http://127.0.0.1:5000")

    driver.get("http://127.0.0.1:5000")
    print("🌐 Dashboard opened. Use the UI to click 'Scrape'.")
    print("💡 Keep this terminal open. Press Ctrl+C to stop safely.\n")

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping bot...")
    finally:
        if driver: driver.quit()


def main():

    print("🚀 Initializing UniPortal Bot...")
    browser_choice = get_browser_choice()
    if not browser_choice:
        print("❌ No browser selected. Exiting.")
        sys.exit(1)

    show_warning(browser_choice)

    # Hidden root for loader management
    loader_root = tk.Tk()
    loader_root.withdraw()
    set_icon(loader_root)

    loader = LoaderOverlay(loader_root)
    loader.protocol("WM_DELETE_WINDOW", lambda: None)
    result_q = queue.Queue()

    def setup_driver_thread():
        try:
            mgr = BrowserManager(browser_choice)
            mgr.kill_processes()
            driver = mgr.setup_driver()
            result_q.put(("success", driver))
        except Exception as e:
            result_q.put(("error", str(e)))

    threading.Thread(target=setup_driver_thread, daemon=True).start()

    def check_driver():
        try:
            status, data = result_q.get_nowait()
            loader.close()
            if status == "error":
                # error dialog dikhao
                loader_root.destroy()
                tk.messagebox.showerror("Browser Error", f"Failed to launch {browser_choice}:\n{data}")
                return
            # success
            loader_root.after(200, lambda: (loader_root.destroy(), start_bot(data, browser_choice)))
        except queue.Empty:
            loader_root.after(150, check_driver)

    loader_root.after(150, check_driver)
    loader_root.mainloop()


if __name__ == "__main__":
    main()