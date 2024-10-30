import os
import pygame
from PIL import Image, ImageTk
from mutagen.mp3 import MP3

class SongPlayer:
    def __init__(self, song_label, play_pause_button, update_progress_callback):
        self.current_song = None
        self.playing = False
        self.paused = False
        self.song_label = song_label
        self.play_pause_button = play_pause_button
        self.update_progress = update_progress_callback

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
            self.load_song_metadata(song_path)
            self.play_pause_button.config(text="⏸")
            self.playing = True
            self.paused = False
            self.update_progress()  # Iniciar la actualización del progreso

    def load_album_art(self, song_path):
        album_art_path = os.path.join(os.path.dirname(song_path), "album_art.jpg")  # Suponiendo que la carátula está en el mismo directorio
        if os.path.exists(album_art_path):
            img = Image.open(album_art_path)
            img = img.resize((100, 100), Image.ANTIALIAS)  # Redimensionar la imagen
            self.album_art.img = ImageTk.PhotoImage(img)
            self.album_art.config(image=self.album_art.img)
        else:
            self.album_art.config(image='')  # Limpiar la imagen si no hay

    def load_song_metadata(self, song_path):
        album_name = "Desconocido"
        self.album_name_label.config(text=f"Álbum: {album_name}")
