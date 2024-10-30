import os
import tkinter as tk
from PIL import Image, ImageTk
import pygame
from mutagen.mp3 import MP3
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

        # Llamada a la nueva función
        self.widgets = create_widgets(self.root, self.select_song, self.previous_song, self.toggle_play_pause, self.next_song)
        self.tree = self.widgets["tree"]
        self.album_art = self.widgets["album_art"]
        self.song_label = self.widgets["song_label"]
        self.play_pause_button = self.widgets["play_pause_button"]
        self.album_name_label = self.widgets["album_name_label"]
        self.progress_frame = self.widgets["progress_frame"]  # Añadido aquí
        self.circle = self.widgets["circle"]  # Añadido aquí
        self.circle_indicator = self.widgets["circle_indicator"]  # Añadido aquí
        self.circle_radius = self.widgets["circle_radius"]  # Añadido aquí

        # Añadir eventos para arrastrar el círculo
        self.circle.bind("<Button-1>", self.start_drag)
        self.circle.bind("<B1-Motion>", self.drag)
        self.circle.bind("<ButtonRelease-1>", self.release)

        self.load_library()
        self.update_progress()  # Añadir actualización de progreso

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
            self.load_song_metadata(song_path)
            self.play_pause_button.config(text="⏸")
            self.playing = True
            self.paused = False
            self.update_progress()  # Iniciar la actualización del progreso

    def update_progress(self):
        if self.playing:
            current_time = pygame.mixer.music.get_pos() / 1000  # tiempo en segundos
            audio = MP3(self.current_song)
            song_length = audio.info.length

            # Calcular el porcentaje del tiempo transcurrido
            progress_percentage = current_time / song_length if song_length > 0 else 0
            progress_width = self.root.winfo_width() * progress_percentage

            # Actualizar la posición del círculo
            self.circle.coords(self.circle_indicator, progress_width - self.circle_radius, 0, progress_width + self.circle_radius, self.circle_radius * 2)
            self.circle.update()

            # Llama a esta función de nuevo después de 1 segundo
            self.root.after(1000, self.update_progress)

    def load_album_art(self, song_path):
        # Cargar la carátula del álbum si está disponible
        album_art_path = os.path.join(os.path.dirname(song_path), "album_art.jpg")  # Suponiendo que la carátula está en el mismo directorio
        if os.path.exists(album_art_path):
            img = Image.open(album_art_path)
            img = img.resize((100, 100), Image.ANTIALIAS)  # Redimensionar la imagen
            self.album_art.img = ImageTk.PhotoImage(img)
            self.album_art.config(image=self.album_art.img)
        else:
            self.album_art.config(image='')  # Limpiar la imagen si no hay

    def load_song_metadata(self, song_path):
        # Actualizar la etiqueta del álbum (esto es opcional y se puede personalizar)
        album_name = "Desconocido"
        self.album_name_label.config(text=f"Álbum: {album_name}")

    def start_drag(self, event):
        self.circle.bind("<B1-Motion>", self.drag)

    def drag(self, event):
        # Mueve el círculo a la posición donde se está arrastrando
        x = event.x
        x = max(0, min(x, self.root.winfo_width()))  # Asegura que no se salga de los límites
        self.circle.coords(self.circle_indicator, x - self.circle_radius, 0, x + self.circle_radius, self.circle_radius * 2)

    def release(self, event):
        # Al soltar el círculo, saltar a la posición correspondiente de la canción
        x = event.x
        x = max(0, min(x, self.root.winfo_width()))  # Asegura que no se salga de los límites
        audio = MP3(self.current_song)
        song_length = audio.info.length
        new_position = (x / self.root.winfo_width()) * song_length
        pygame.mixer.music.seek(new_position)  # Saltar a la nueva posición
        self.update_progress()  # Actualizar la barra de progreso

    def previous_song(self):
        current_index = self.song_list.index(self.current_song)
        if current_index > 0:
            self.play_song(self.song_list[current_index - 1])

    def next_song(self):
        current_index = self.song_list.index(self.current_song)
        if current_index < len(self.song_list) - 1:
            self.play_song(self.song_list[current_index + 1])

if __name__ == "__main__":
    root = tk.Tk()
    player = MP3Player(root)
    root.mainloop()
