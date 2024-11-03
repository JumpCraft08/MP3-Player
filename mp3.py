import os
import json
import pygame
import tkinter as tk
from tkinter import Toplevel, ttk
from mutagen.mp3 import MP3

# Inicializa todos los módulos de Pygame
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

        # Configurar la interfaz
        self.lista = tk.Listbox(master, width=50, height=15, bg="#ffffff", selectbackground="#007BFF", font=("Arial", 12))
        self.lista.pack(pady=20)
        self.lista.bind('<ButtonRelease-1>', self.reproducir_cancion_seleccionada)

        # Marco para mostrar la canción actual
        self.marco_bajo = tk.Frame(master, bg="#3e444f")
        self.marco_bajo.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(10, 10))

        # Marco para los textos
        self.marco_textos = tk.Frame(self.marco_bajo, bg="#3e444f")
        self.marco_textos.pack(side=tk.LEFT, padx=10)

        # Etiquetas para el título de la canción y el artista
        self.titulo_cancion = tk.Label(self.marco_textos, text="No hay canción sonando", bg="#3e444f", fg="#ffffff", font=("Arial", 14, "bold"), anchor='w')
        self.titulo_cancion.pack(side=tk.TOP, fill=tk.X)

        self.artista_cancion = tk.Label(self.marco_textos, text="", bg="#3e444f", fg="#a9a9a9", font=("Arial", 12))
        self.artista_cancion.pack(side=tk.TOP)

        # Marco para los botones de control
        self.marco_botones = tk.Frame(self.marco_bajo, bg="#3e444f")
        self.marco_botones.pack(side=tk.RIGHT)

        # Botones de control
        self.boton_anterior = tk.Button(self.marco_botones, text="⏮️", command=self.cancion_anterior, bg="#007BFF", fg="#ffffff", font=("Arial", 14), width=3)
        self.boton_anterior.grid(row=0, column=0, padx=5)

        self.boton_pausa_reproducir = tk.Button(self.marco_botones, text="▶️", command=self.pausar_reproducir, bg="#007BFF", fg="#ffffff", font=("Arial", 14), width=3)
        self.boton_pausa_reproducir.grid(row=0, column=1, padx=5)

        self.boton_siguiente = tk.Button(self.marco_botones, text="⏭️", command=self.cancion_siguiente, bg="#007BFF", fg="#ffffff", font=("Arial", 14), width=3)
        self.boton_siguiente.grid(row=0, column=2, padx=5)

        # Menú contextual para ajustes
        self.menu_contextual = tk.Menu(master, tearoff=0)
        self.menu_contextual.add_command(label="Ajustes", command=self.abrir_ajustes)
        self.master.bind("<Button-3>", self.mostrar_menu_contextual)

        self.cargar_ajustes()  # Cargar ajustes al iniciar
        self.cargar_mp3()  # Cargar archivos al iniciar
        self.configurar_evento_finalizacion()  # Configurar el evento de finalización

    def mostrar_menu_contextual(self, event):
        self.menu_contextual.post(event.x_root, event.y_root)

    def abrir_ajustes(self):
        ventana_ajustes = Toplevel(self.master)
        ventana_ajustes.title("Ajustes")
        ventana_ajustes.geometry("300x200")

        etiqueta_mostrar_por = tk.Label(ventana_ajustes, text="Mostrar por:")
        etiqueta_mostrar_por.pack(pady=10)

        self.combo_mostrar_por_ajustes = ttk.Combobox(ventana_ajustes, state='readonly', values=["Canción"])
        self.combo_mostrar_por_ajustes.current(0)  # Establecer el valor actual
        self.combo_mostrar_por_ajustes.pack(pady=10)

        boton_guardar = tk.Button(ventana_ajustes, text="Guardar", command=lambda: self.guardar_ajustes(ventana_ajustes))
        boton_guardar.pack(pady=10)

    def cargar_ajustes(self):
        if os.path.exists('ajustes.json'):
            with open('ajustes.json', 'r') as archivo:
                ajustes = json.load(archivo)
                self.modo_mostrar_por = ajustes.get("modo_mostrar_por", "Canción")

    def guardar_ajustes(self, ventana):
        ajustes = {"modo_mostrar_por": self.modo_mostrar_por}
        with open('ajustes.json', 'w') as archivo:
            json.dump(ajustes, archivo)
        ventana.destroy()

    def configurar_evento_finalizacion(self):
        self.master.after(100, self.check_music_end)  # Comienza a comprobar el fin de la música

    def check_music_end(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:  # Verifica si la música ha terminado
                self.cancion_siguiente()  # Reproduce la siguiente canción
        self.master.after(100, self.check_music_end)  # Revisa el evento cada 100 ms

    def cargar_mp3(self):
        directorio = 'files'  # Carpeta estática
        self.archivos_mp3 = []
        self.lista.delete(0, tk.END)  # Limpia la lista existente

        for root, _, files in os.walk(directorio):
            for file in files:
                if file.endswith(".mp3"):
                    ruta_completa = os.path.join(root, file)
                    self.archivos_mp3.append(ruta_completa)
                    self.lista.insert(tk.END, file)  # Mostrar solo canciones

    def reproducir_cancion_seleccionada(self, event):
        seleccion = self.lista.curselection()
        if seleccion:
            self.indice_actual = seleccion[0]
            self.archivo_actual = self.archivos_mp3[self.indice_actual]
            pygame.mixer.music.load(self.archivo_actual)
            pygame.mixer.music.play()
            self.actualizar_info_cancion()

    def actualizar_info_cancion(self):
        if self.archivo_actual:
            nombre_archivo = os.path.basename(self.archivo_actual)
            nombre_sin_extension = os.path.splitext(nombre_archivo)[0]  # Elimina la extensión
            max_length = 24  # Longitud máxima del texto

            # Recorta el nombre si es necesario
            if len(nombre_sin_extension) > max_length:
                nombre_sin_extension = nombre_sin_extension[:max_length - 3] + "..."

            self.titulo_cancion.config(text=nombre_sin_extension)

            try:
                audio = MP3(self.archivo_actual)
                artista = audio.get('TPE1', ["Artista desconocido"])[0]
                self.artista_cancion.config(text=artista)
            except Exception:
                self.artista_cancion.config(text="Artista desconocido")

    def pausar_reproducir(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.boton_pausa_reproducir.config(text="▶️")  # Cambia a botón de reproducir
        else:
            pygame.mixer.music.unpause()
            self.boton_pausa_reproducir.config(text="⏸️")  # Cambia a botón de pausa

    def cancion_anterior(self):
        if self.indice_actual > 0:
            self.indice_actual -= 1
            self.cargar_y_reproducir_cancion()

    def cancion_siguiente(self):
        if self.indice_actual < len(self.archivos_mp3) - 1:
            self.indice_actual += 1
            self.cargar_y_reproducir_cancion()

    def cargar_y_reproducir_cancion(self):
        self.archivo_actual = self.archivos_mp3[self.indice_actual]
        pygame.mixer.music.load(self.archivo_actual)
        pygame.mixer.music.play()
        self.lista.selection_clear(0, tk.END)
        self.lista.selection_set(self.indice_actual)
        self.lista.activate(self.indice_actual)
        self.actualizar_info_cancion()

if __name__ == "__main__":
    root = tk.Tk()
    app = ReproductorMP3(root)
    root.mainloop()
