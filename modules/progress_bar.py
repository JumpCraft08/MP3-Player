import pygame
import tkinter as tk

class ProgressBar:
    def __init__(self, master, update_callback):
        self.master = master
        self.update_callback = update_callback
        self.is_dragging = False
        
        # Crea el slider
        self.progress = tk.DoubleVar()
        self.slider = tk.Scale(master, variable=self.progress, from_=0, to=100, orient="horizontal", showvalue=False)
        self.slider.pack(fill=tk.X, padx=10)

        self.slider.bind("<ButtonPress>", self.start_drag)
        self.slider.bind("<ButtonRelease>", self.end_drag)

    def start_drag(self, event):
        self.is_dragging = True

    def end_drag(self, event):
        self.is_dragging = False
        self.update_callback(self.progress.get())  # Llama a seek_music al soltar el slider

    def update(self, current_time, total_time):
        if not self.is_dragging:  # Solo actualiza si no se está arrastrando
            percentage = (current_time / total_time) * 100 if total_time > 0 else 0
            self.progress.set(percentage)
