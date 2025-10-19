#!/usr/bin/env python3
# CF-Soundboard (Single Script)

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import pygame

APP_NAME = "CF-Soundboard"
SOUND_DIR = os.path.join(os.path.dirname(__file__), "sounds")

class SoundboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME}")
        self.geometry("420x560")
        self.configure(bg="#1e1e1e")

        # init audio
        try:
            pygame.mixer.init()
        except Exception as e:
            messagebox.showerror("Audio Error", str(e))

        # UI
        ttk.Label(self, text=APP_NAME, font=("Menlo", 16, "bold")).pack(pady=8)
        ttk.Label(self, text="ใส่ไฟล์ .mp3 หรือ .wav ในโฟลเดอร์ sounds/", wraplength=300).pack(pady=2)

        control_frame = tk.Frame(self, bg="#1e1e1e")
        control_frame.pack(pady=6)
        ttk.Button(control_frame, text="Stop", command=self.stop_audio).pack(side="left", padx=4)
        ttk.Button(control_frame, text="Refresh", command=self.refresh_sounds).pack(side="left", padx=4)
        ttk.Button(control_frame, text="Open Folder", command=self.open_folder).pack(side="left", padx=4)

        vol_frame = tk.Frame(self, bg="#1e1e1e")
        vol_frame.pack(pady=4, fill="x", padx=10)
        ttk.Label(vol_frame, text="Volume").pack(side="left", padx=4)
        self.vol = tk.DoubleVar(value=0.8)
        scale = ttk.Scale(vol_frame, from_=0.0, to=1.0, variable=self.vol, command=self.change_volume)
        scale.pack(fill="x", expand=True, padx=8)
        pygame.mixer.music.set_volume(self.vol.get())

        self.canvas = tk.Canvas(self, bg="#1e1e1e", highlightthickness=0)
        self.frame = tk.Frame(self.canvas, bg="#1e1e1e")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.canvas_frame = self.canvas.create_window((0,0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", self.update_scroll)
        self.canvas.bind("<Configure>", self.resize_canvas)

        self.sound_buttons = []
        self.refresh_sounds()

    def change_volume(self, *args):
        pygame.mixer.music.set_volume(self.vol.get())

    def stop_audio(self):
        pygame.mixer.music.stop()

    def open_folder(self):
        if sys.platform == "darwin":
            os.system(f'open "{SOUND_DIR}"')
        else:
            messagebox.showinfo("Path", SOUND_DIR)

    def refresh_sounds(self):
        for b in self.sound_buttons:
            b.destroy()
        self.sound_buttons.clear()

        if not os.path.isdir(SOUND_DIR):
            os.makedirs(SOUND_DIR, exist_ok=True)

        files = sorted(f for f in os.listdir(SOUND_DIR)
                       if f.lower().endswith((".mp3", ".wav")))
        if not files:
            lbl = ttk.Label(self.frame, text="(ไม่มีไฟล์เสียงในโฟลเดอร์ sounds/)", anchor="center")
            lbl.pack(pady=12)
            self.sound_buttons.append(lbl)
            return

        for f in files:
            path = os.path.join(SOUND_DIR, f)
            name = os.path.splitext(f)[0]
            btn = ttk.Button(self.frame, text=name, command=lambda p=path: self.play_audio(p))
            btn.pack(fill="x", pady=4)
            self.sound_buttons.append(btn)

    def play_audio(self, path):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        except Exception as e:
            messagebox.showerror("Playback Error", str(e))

    def update_scroll(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def resize_canvas(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

if __name__ == "__main__":
    app = SoundboardApp()
    app.mainloop()

