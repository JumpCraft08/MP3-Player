import os
import tkinter as tk
import pygame
from mutagen.mp3 import MP3
from modules.style import create_widgets
from modules.song import SongPlayer  # Importar la clase SongPlayer

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

        self.dragging = False

        # Llamada a la nueva función
        self.widgets = create_widgets(self.root, self.select_song, self.previous_song, self.toggle_play_pause, self.next_song)
        self.tree = self.widgets["tree"]
        self.album_art = self.widgets["album_art"]
        self.song_label = self.widgets["song_label"]
        self.play_pause_button = self.widgets["play_pause_button"]
        self.album_name_label = self.widgets["album_name_label"]
        self.progress_frame = self.widgets["progress_frame"]
        self.circle = self.widgets["circle"]
        self.circle_indicator = self.widgets["circle_indicator"]
        self.circle_radius = self.widgets["circle_radius"]

        # Inicializar el reproductor de canciones
        self.song_player = SongPlayer(self.song_label, self.play_pause_button, self.update_progress)

        # Añadir eventos para arrastrar el círculo
        self.circle.bind("<Button-1>", self.start_drag)
        self.circle.bind("<B1-Motion>", self.drag)
        self.circle.bind("<ButtonRelease-1>", self.release)

        self.load_library()
        self.update_progress()  # Iniciar la actualización del progreso al principio

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
            self.song_player.play_song(song_path)  # Usar el método play_song del objeto SongPlayer

    def toggle_play_pause(self):
        self.song_player.toggle_play_pause()  # Usar el método toggle_play_pause del objeto SongPlayer

    def update_progress(self):
        if self.song_player.playing:
            current_time = pygame.mixer.music.get_pos() / 1000  # tiempo en segundos
            audio = MP3(self.song_player.current_song)
            song_length = audio.info.length

            if song_length > 0:
                # Calcular el porcentaje del tiempo transcurrido
                progress_percentage = current_time / song_length
                progress_width = self.root.winfo_width() * progress_percentage

                # Actualizar la posición del círculo
                self.circle.coords(self.circle_indicator, progress_width - self.circle_radius, 0, progress_width + self.circle_radius, self.circle_radius * 2)

            # Llama a esta función de nuevo después de 100 ms
            self.root.after(100, self.update_progress)

    def start_drag(self, event):
        self.dragging = True

    def drag(self, event):
        if self.dragging:
            # Mueve el círculo a la posición donde se está arrastrando
            x = event.x
            x = max(0, min(x, self.root.winfo_width()))  # Asegura que no se salga de los límites
            self.circle.coords(self.circle_indicator, x - self.circle_radius, 0, x + self.circle_radius, self.circle_radius * 2)

    def release(self, event):
        if self.dragging:
            self.dragging = False  # Dejar de arrastrar
            # Al soltar el círculo, saltar a la posición correspondiente de la canción
            x = event.x
            x = max(0, min(x, self.root.winfo_width()))  # Asegura que no se salga de los límites
            audio = MP3(self.song_player.current_song)
            song_length = audio.info.length
            new_position = (x / self.root.winfo_width()) * song_length

            # Reproducir la canción desde la nueva posición
            pygame.mixer.music.stop()  # Detener la canción actual
            pygame.mixer.music.load(self.song_player.current_song)  # Cargar la canción nuevamente
            pygame.mixer.music.play(0, new_position)  # Reproducir desde la nueva posición

            # Actualiza el progreso para reflejar la nueva posición
            self.update_progress()  # Actualizar la barra de progreso

    def previous_song(self):
        current_index = self.song_list.index(self.song_player.current_song)
        if current_index > 0:
            self.song_player.play_song(self.song_list[current_index - 1])

    def next_song(self):
        current_index = self.song_list.index(self.song_player.current_song)
        if current_index < len(self.song_list) - 1:
            self.song_player.play_song(self.song_list[current_index + 1])

if __name__ == "__main__":
    root = tk.Tk()
    player = MP3Player(root)
    root.mainloop()
