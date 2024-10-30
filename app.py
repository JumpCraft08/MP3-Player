import os
import tkinter as tk
from PIL import Image, ImageTk
import pygame
from modules.style import create_widgets

# Inicializar pygame mixer
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "files")

class MP3Player:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor MP3 - Biblioteca")
        self.root.geometry("800x600")
        self.root.config(bg="#2C3E50")

        self.current_song = None
        self.playing = False
        self.paused = False
        self.song_list = []

        # Variables para mostrar la canción y progreso
        self.album_art = None
        self.album_image = None
        self.song_duration = 0

        # Llamada a la nueva función
        self.widgets = create_widgets(self.root, self.select_song, self.previous_song, self.toggle_play_pause, self.next_song)
        self.tree = self.widgets["tree"]
        self.album_art = self.widgets["album_art"]
        self.song_label = self.widgets["song_label"]
        self.progress_var = self.widgets["progress_var"]
        self.progress_bar = self.widgets["progress_bar"]
        self.play_pause_button = self.widgets["play_pause_button"]

        self.load_library()


    def load_library(self):
        self.song_list = []
        self.add_folder_to_tree("", BASE_PATH)

    def add_folder_to_tree(self, parent, path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                folder_id = self.tree.insert(parent, "end", text=item, values=("", item_path))
                self.add_folder_to_tree(folder_id, item_path)
            elif item.endswith(".mp3"):
                song_id = self.tree.insert(parent, "end", text=item, values=(item, item_path))
                self.song_list.append(item_path)

    def select_song(self, event):
        selected_item = self.tree.selection()[0]
        song_path = self.tree.item(selected_item, "values")[1]
        if song_path.endswith(".mp3"):
            self.play_song(song_path)

    def toggle_play_pause(self):
        if self.playing:
            if self.paused:
                pygame.mixer.music.unpause()
                self.play_pause_button.config(text="⏸")
                self.paused = False
            else:
                pygame.mixer.music.pause()
                self.play_pause_button.config(text="▶️")
                self.paused = True
        elif self.current_song:
            self.play_song(self.current_song)

    def play_song(self, song_path=None):
        if song_path:
            self.current_song = song_path
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.song_label.config(text=os.path.basename(song_path).replace(".mp3", ""))
            self.load_album_art(song_path)
            self.play_pause_button.config(text="⏸")
            self.playing = True
            self.paused = False
            self.update_progress()

    def load_album_art(self, song_path):
        album_dir = os.path.dirname(song_path)
        cover_path = os.path.join(album_dir, "cover.jpg")

        if os.path.exists(cover_path):
            album_image = Image.open(cover_path)
            album_image = album_image.resize((100, 100), Image.ANTIALIAS)
            self.album_image = ImageTk.PhotoImage(album_image)
            self.album_art.config(image=self.album_image)
        else:
            self.album_art.config(image="")  # Placeholder si no hay imagen

    def update_progress(self):
        if self.playing and not self.paused:
            self.progress_var.set(pygame.mixer.music.get_pos() / 1000)  # Tiempo en segundos
            self.root.after(1000, self.update_progress)

    def previous_song(self):
        if self.current_song:
            current_index = self.song_list.index(self.current_song)
            previous_index = (current_index - 1) % len(self.song_list)
            self.play_song(self.song_list[previous_index])

    def next_song(self):
        if self.current_song:
            current_index = self.song_list.index(self.current_song)
            next_index = (current_index + 1) % len(self.song_list)
            self.play_song(self.song_list[next_index])

# Crear y ejecutar la aplicación
root = tk.Tk()
app = MP3Player(root)
root.mainloop()
