import tkinter as tk
from tkinter import messagebox
import pyautogui
import threading
import time

class DiscordAutomatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord GUI Text Automator")
        self.root.geometry("400x340")
        self.root.resizable(False, False)
        
        # State variables
        self.is_running = False
        self.automation_thread = None
        
        # Configure PyAutoGUI fail-safe
        pyautogui.FAILSAFE = True
        
        self.create_widgets()

    def create_widgets(self):
        # Instructions Label
        instructions = (
            "How to use:\n"
            "1. Enter your text and interval below.\n"
            "2. Click 'Start Automation'.\n"
            "3. You have 5 seconds to click inside your Discord text box.\n"
            "⚠️ Emergency Stop: Slam mouse to TOP-LEFT corner of screen."
        )
        lbl_info = tk.Label(self.root, text=instructions, fg="darkblue", justify="left", wraplength=360)
        lbl_info.pack(pady=15)

        # Message Entry Frame
        frame_msg = tk.Frame(self.root)
        frame_msg.pack(fill="x", padx=20, pady=5)
        
        lbl_msg = tk.Label(frame_msg, text="Message to send:")
        lbl_msg.pack(anchor="w")
        self.txt_message = tk.Entry(frame_msg, font=("Arial", 11))
        self.txt_message.pack(fill="x", pady=2)
        self.txt_message.insert(0, "Automated message text")

        # Interval Entry Frame
        frame_int = tk.Frame(self.root)
        frame_int.pack(fill="x", padx=20, pady=5)
        
        lbl_int = tk.Label(frame_int, text="Interval (in seconds):")
        lbl_int.pack(anchor="w")
        self.txt_interval = tk.Entry(frame_int, width=10, font=("Arial", 11))
        self.txt_interval.pack(anchor="w", pady=2)
        self.txt_interval.insert(0, "60")

        # Status Label (Shows running status and live countdown)
        self.lbl_status = tk.Label(self.root, text="Status: Stopped", fg="red", font=("Arial", 11, "bold"))
        self.lbl_status.pack(pady=15)

        # Control Buttons
        self.btn_start = tk.Button(self.root, text="Start Automation", bg="green", fg="white", font=("Arial", 10, "bold"), command=self.start_automation)
        self.btn_start.pack(side="left", padx=40, pady=5)

        self.btn_stop = tk.Button(self.root, text="Stop App", bg="red", fg="white", font=("Arial", 10, "bold"), state="disabled", command=self.stop_automation)
        self.btn_stop.pack(side="right", padx=40, pady=5)

    def start_automation(self):
        try:
            # Force interval to be a clean whole integer for perfect second-by-second countdowns
            interval = int(self.txt_interval.get())
            if interval <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid whole number of seconds greater than 0.")
            return

        message = self.txt_message.get().strip()
        if not message:
            messagebox.showerror("Invalid Input", "Please enter a message to send.")
            return

        self.is_running = True
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.lbl_status.config(text="Status: Preparing (5s delay)...", fg="orange")

        self.automation_thread = threading.Thread(target=self.automation_loop, args=(message, interval), daemon=True)
        self.automation_thread.start()

    def stop_automation(self):
        self.is_running = False
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.lbl_status.config(text="Status: Stopped", fg="red")

    def automation_loop(self, message, interval):
        # 5-second preparation countdown
        for i in range(5, 0, -1):
            if not self.is_running:
                return
            self.lbl_status.config(text=f"Status: Click into Discord box! ({i}s)...")
            time.sleep(1)

        try:
            while self.is_running:
                # Type message with a slight interval between characters to ensure Discord registers it
                pyautogui.write(message, interval=0.01)
                pyautogui.press('enter')

                # Live countdown sequence until next message
                for remaining in range(interval, 0, -1):
                    if not self.is_running:
                        return
                    self.lbl_status.config(
                        text=f"Status: Running | Next message in {remaining}s", 
                        fg="green"
                    )
                    time.sleep(1)

        except pyautogui.FailSafeException:
            self.root.after(0, self.handle_failsafe)

    def handle_failsafe(self):
        self.stop_automation()
        messagebox.showwarning("Fail-Safe Triggered", "Automation stopped because you moved the mouse to the corner of the screen.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordAutomatorApp(root)
    root.mainloop()
