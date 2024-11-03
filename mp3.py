import os
import json
import pygame
import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
from mutagen.mp3 import MP3
from modules.add_music import añadir_musica
from modules.license import abrir_informacion

pygame.init()
pygame.mixer.init()

class ReproductorMP3:
    def __init__(self, master):
        self.master = master
        self.master.title("Reproductor MP3")
        self.master.geometry("450x400")
        self.master.configure(bg="#282c34")

        self.archivos_mp3 = []
        self.archivo_actual = None
        self.indice_actual = 0

        self.MUSICA_TERMINADA = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSICA_TERMINADA)

        self.setup_ui()
        self.modo_mostrar_por = self.cargar_ajustes()
        self.cargar_mp3()
        self.configurar_evento_finalizacion()

    def setup_ui(self):
        self.frame_lista = tk.Frame(self.master, bg="#282c34")
        self.frame_lista.pack(pady=20, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame_lista, bg="#282c34", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.frame_lista, orient="vertical", command=self.canvas.yview, bg="#282c34")
        self.scrollable_frame = tk.Frame(self.canvas, bg="#282c34")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.marco_bajo = tk.Frame(self.master, bg="#3e444f")
        self.marco_bajo.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(10, 10))

        self.marco_textos = tk.Frame(self.marco_bajo, bg="#3e444f")
        self.marco_textos.pack(side=tk.LEFT, padx=10)

        self.titulo_cancion = tk.Label(self.marco_textos, text="No hay canción sonando", bg="#3e444f", fg="#ffffff", font=("Arial", 14, "bold"), anchor='w')
        self.titulo_cancion.pack(side=tk.TOP, fill=tk.X)

        self.artista_cancion = tk.Label(self.marco_textos, text="", bg="#3e444f", fg="#a9a9a9", font=("Arial", 12))
        self.artista_cancion.pack(side=tk.TOP)

        self.marco_botones = tk.Frame(self.marco_bajo, bg="#3e444f")
        self.marco_botones.pack(side=tk.RIGHT)

        self.boton_anterior = self.crear_boton(self.marco_botones, "⏮️", lambda: self.cambiar_cancion(-1))
        self.boton_pausa_reproducir = self.crear_boton(self.marco_botones, "▶️", self.pausar_reproducir)
        self.boton_siguiente = self.crear_boton(self.marco_botones, "⏭️", lambda: self.cambiar_cancion(1))

        self.menu_contextual = tk.Menu(self.master, tearoff=0)
        self.menu_contextual.add_command(label="Ajustes", command=self.abrir_ajustes)
        self.menu_contextual.add_command(label="Añadir música", command=self.añadir_musica)
        self.menu_contextual.add_command(label="Información", command=lambda: abrir_informacion(self.master))
        self.master.bind("<Button-3>", self.mostrar_menu_contextual)

    def crear_boton(self, parent, texto, comando):
        boton = tk.Button(parent, text=texto, command=comando, bg="#007BFF", fg="#ffffff", font=("Arial", 14), width=3)
        boton.grid(row=0, column=len(parent.grid_slaves()), padx=5)
        return boton

    def mostrar_menu_contextual(self, event):
        self.menu_contextual.post(event.x_root, event.y_root)

    def añadir_musica(self):
        añadir_musica(self.cargar_mp3)

    def abrir_ajustes(self):
        ventana_ajustes = Toplevel(self.master)
        ventana_ajustes.title("Ajustes")
        ventana_ajustes.geometry("300x200")

        tk.Label(ventana_ajustes, text="Mostrar por:").pack(pady=10)
        self.combo_mostrar_por_ajustes = ttk.Combobox(ventana_ajustes, state='readonly', values=["Canción"])
        self.combo_mostrar_por_ajustes.current(0)
        self.combo_mostrar_por_ajustes.pack(pady=10)

        tk.Button(ventana_ajustes, text="Guardar", command=lambda: self.guardar_ajustes(ventana_ajustes)).pack(pady=10)

    def cargar_ajustes(self):
        if os.path.exists('ajustes.json'):
            with open('ajustes.json', 'r') as archivo:
                ajustes = json.load(archivo)
                return ajustes.get("modo_mostrar_por", "Canción")
        return "Canción"

    def guardar_ajustes(self, ventana):
        ajustes = {"modo_mostrar_por": self.modo_mostrar_por}
        with open('ajustes.json', 'w') as archivo:
            json.dump(ajustes, archivo)
        ventana.destroy()

    def configurar_evento_finalizacion(self):
        self.master.after(100, self.check_music_end)

    def check_music_end(self):
        for event in pygame.event.get():
            if event.type == self.MUSICA_TERMINADA:
                self.cambiar_cancion(1)
        self.master.after(100, self.check_music_end)

    def cargar_mp3(self):
        directorio = 'files'
        self.archivos_mp3.clear()
        self.limpiar_lista()

        for root, _, files in os.walk(directorio):
            for file in files:
                if file.endswith(".mp3"):
                    ruta_completa = os.path.join(root, file)
                    self.archivos_mp3.append(ruta_completa)
                    self.crear_label_cancion(file, ruta_completa)

    def limpiar_lista(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def crear_label_cancion(self, file, ruta_completa):
        artista = self.obtener_artista(ruta_completa)

        frame_label = tk.Frame(self.scrollable_frame, bg="#3e444f")
        frame_label.pack(pady=5, padx=5, fill=tk.X)

        titulo_label = tk.Label(frame_label, text=file, bg="#3e444f", fg="#ffffff", font=("Arial", 12, "bold"), anchor='w')
        titulo_label.pack(fill=tk.X)

        artista_label = tk.Label(frame_label, text=artista, bg="#3e444f", fg="#ffffff", font=("Arial", 10), anchor='w')
        artista_label.pack(anchor='w')

        self.asignar_evento_click(frame_label, titulo_label, artista_label)

    def asignar_evento_click(self, frame_label, titulo_label, artista_label):
        index = len(self.archivos_mp3) - 1  # Use el último índice disponible
        frame_label.bind('<Button-1>', lambda event: self.reproducir_cancion(index))
        titulo_label.bind('<Button-1>', lambda event: self.reproducir_cancion(index))
        artista_label.bind('<Button-1>', lambda event: self.reproducir_cancion(index))

    def obtener_artista(self, ruta):
        try:
            audio = MP3(ruta)
            return audio.get('TPE1', ["Artista desconocido"])[0] or "Artista desconocido"
        except Exception:
            return "Artista desconocido"

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    def reproducir_cancion(self, index):
        if 0 <= index < len(self.archivos_mp3):
            self.indice_actual = index
            self.archivo_actual = self.archivos_mp3[self.indice_actual]
            self.intentar_reproducir()

    def intentar_reproducir(self):
        try:
            pygame.mixer.music.load(self.archivo_actual)
            pygame.mixer.music.play()
            self.actualizar_info_cancion()
            self.boton_pausa_reproducir.config(text="⏸️")
        except Exception as e:
            self.mostrar_error("No se pudo reproducir la canción", str(e))

    def mostrar_error(self, mensaje, detalle):
        messagebox.showerror(mensaje, detalle)

    def actualizar_info_cancion(self):
        if self.archivo_actual:
            nombre_archivo = os.path.basename(self.archivo_actual)
            nombre_sin_extension = os.path.splitext(nombre_archivo)[0]
            self.titulo_cancion.config(text=(nombre_sin_extension[:21] + '...') if len(nombre_sin_extension) > 24 else nombre_sin_extension)

            artista = self.obtener_artista(self.archivo_actual)
            self.artista_cancion.config(text=artista)

    def pausar_reproducir(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.boton_pausa_reproducir.config(text="▶️")
        else:
            pygame.mixer.music.unpause()
            self.boton_pausa_reproducir.config(text="⏸️")

    def cambiar_cancion(self, direccion):
        nuevo_indice = self.indice_actual + direccion
        if 0 <= nuevo_indice < len(self.archivos_mp3):
            self.reproducir_cancion(nuevo_indice)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReproductorMP3(root)
    root.mainloop()
