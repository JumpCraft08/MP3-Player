import os
import tkinter as tk
from tkinter import Listbox, END, Scrollbar
import pygame

# Inicializar pygame mixer
pygame.mixer.init()

# Ruta base para las canciones (ubicada en la misma carpeta que el archivo .py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "files")

class MP3Player:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor MP3")
        self.root.geometry("600x400")
        self.root.config(bg="#2C3E50")

        # Variables de reproducción
        self.current_song = None
        self.playing = False
        self.paused = False

        # Crear widgets de interfaz y cargar canciones
        self.create_widgets()
        self.load_songs()

    def create_widgets(self):
        # Etiqueta de título
        title_label = tk.Label(self.root, text="Reproductor de MP3", font=("Arial", 20, "bold"), bg="#2C3E50", fg="#ECF0F1")
        title_label.pack(pady=10)

        # Lista de canciones con barra de desplazamiento
        frame_listbox = tk.Frame(self.root, bg="#2C3E50")
        frame_listbox.pack(pady=10)

        scrollbar = Scrollbar(frame_listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.song_listbox = Listbox(frame_listbox, selectmode=tk.SINGLE, bg="#34495E", fg="white", font=("Arial", 12), yscrollcommand=scrollbar.set, width=50, height=12)
        self.song_listbox.pack()
        scrollbar.config(command=self.song_listbox.yview)

        # Botones de control en un frame
        frame_controls = tk.Frame(self.root, bg="#2C3E50")
        frame_controls.pack(pady=20)

        # Botón de canción anterior
        self.prev_button = tk.Button(frame_controls, text="⏮", command=self.previous_song, bg="#2C3E50", fg="white", font=("Arial", 20), borderwidth=0, activebackground="#2C3E50")
        self.prev_button.grid(row=0, column=0, padx=20)

        # Botón central de reproducción/pausa
        self.play_pause_button = tk.Button(frame_controls, text="▶️", command=self.toggle_play_pause, bg="#2C3E50", fg="white", font=("Arial", 20), borderwidth=0, activebackground="#2C3E50")
        self.play_pause_button.grid(row=0, column=1, padx=20)

        # Botón de canción siguiente
        self.next_button = tk.Button(frame_controls, text="⏭", command=self.next_song, bg="#2C3E50", fg="white", font=("Arial", 20), borderwidth=0, activebackground="#2C3E50")
        self.next_button.grid(row=0, column=2, padx=20)

    def load_songs(self):
        """ Cargar todas las canciones en la lista de canciones. """
        for root, dirs, files in os.walk(BASE_PATH):
            for file in files:
                if file.endswith(".mp3"):
                    song_path = os.path.join(root, file)
                    song_display_name = song_path.replace(BASE_PATH + os.sep, "")  # Nombre relativo
                    self.song_listbox.insert(END, song_display_name)

    def toggle_play_pause(self):
        """ Alternar entre reproducir y pausar la canción. """
        if self.playing:
            if self.paused:
                pygame.mixer.music.unpause()
                self.play_pause_button.config(text="⏸")
                self.paused = False
            else:
                pygame.mixer.music.pause()
                self.play_pause_button.config(text="▶️")
                self.paused = True
        else:
            self.play_song()

    def play_song(self):
        """ Reproducir la canción seleccionada. """
        selected_song = self.song_listbox.get(tk.ACTIVE)
        song_path = os.path.join(BASE_PATH, selected_song)

        # Detener cualquier canción que esté sonando
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.play_pause_button.config(text="⏸")
        self.current_song = selected_song
        self.playing = True
        self.paused = False

    def stop_song(self):
        """ Detener la canción en reproducción. """
        pygame.mixer.music.stop()
        self.play_pause_button.config(text="▶️")
        self.playing = False
        self.current_song = None

    def previous_song(self):
        """ Reproducir la canción anterior. """
        current_selection = self.song_listbox.curselection()
        if not current_selection:
            previous_index = self.song_listbox.size() - 1
        else:
            current_index = current_selection[0]
            previous_index = (current_index - 1) % self.song_listbox.size()

        self.song_listbox.select_clear(0, END)
        self.song_listbox.select_set(previous_index)
        self.song_listbox.activate(previous_index)
        self.play_song()

    def next_song(self):
        """ Reproducir la siguiente canción. """
        current_selection = self.song_listbox.curselection()
        if not current_selection:
            next_index = 0
        else:
            current_index = current_selection[0]
            next_index = (current_index + 1) % self.song_listbox.size()

        self.song_listbox.select_clear(0, END)
        self.song_listbox.select_set(next_index)
        self.song_listbox.activate(next_index)
        self.play_song()

# Crear y ejecutar la aplicación
root = tk.Tk()
app = MP3Player(root)
root.mainloop()
