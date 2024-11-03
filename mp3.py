import os
import json
import pygame
import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from mutagen.mp3 import MP3

# Inicializa Pygame
pygame.mixer.init()
pygame.init()  # Inicializa todos los módulos de Pygame, incluido el sistema de video

class ReproductorMP3:
    def __init__(self, master):
        self.master = master
        self.master.title("Reproductor MP3")

        # Cambiar el tamaño de la ventana
        self.master.geometry("450x400")
        self.master.configure(bg="#282c34")

        self.archivos_mp3 = []
        self.archivo_actual = None
        self.indice_actual = 0
        self.modo_mostrar_por = "Canción"  # Modo por defecto

        # Configurar la interfaz
        self.lista = tk.Listbox(master, width=50, height=15, bg="#ffffff", selectbackground="#007BFF", font=("Arial", 12))
        self.lista.pack(pady=20)

        # Añadir evento de clic a la lista
        self.lista.bind('<ButtonRelease-1>', self.reproducir_cancion_seleccionada)

        # Marco para mostrar la canción actual
        self.marco_bajo = tk.Frame(master, bg="#3e444f")
        self.marco_bajo.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(10, 10))

        # Marco para los textos
        self.marco_textos = tk.Frame(self.marco_bajo, bg="#3e444f")
        self.marco_textos.pack(side=tk.LEFT, padx=10)

        # Etiquetas para el título de la canción y el artista
        self.titulo_cancion = tk.Label(self.marco_textos, text="No hay canción sonando", bg="#3e444f", fg="#ffffff", font=("Arial", 14, "bold"))
        self.titulo_cancion.pack(side=tk.TOP)

        # Etiqueta para el artista debajo del título
        self.artista_cancion = tk.Label(self.marco_textos, text="", bg="#3e444f", fg="#a9a9a9", font=("Arial", 12))
        self.artista_cancion.pack(side=tk.TOP)

        # Marco para los botones de control
        self.marco_botones = tk.Frame(self.marco_bajo, bg="#3e444f")
        self.marco_botones.pack(side=tk.RIGHT)

        # Botones más pequeños
        self.boton_anterior = tk.Button(self.marco_botones, text="⏮️", command=self.cancion_anterior, bg="#007BFF", fg="#ffffff", font=("Arial", 14), width=3, activebackground="#0056b3")
        self.boton_anterior.grid(row=0, column=0, padx=5)

        self.boton_pausa_reproducir = tk.Button(self.marco_botones, text="▶️", command=self.pausar_reproducir, bg="#007BFF", fg="#ffffff", font=("Arial", 14), width=3, activebackground="#0056b3")
        self.boton_pausa_reproducir.grid(row=0, column=1, padx=5)

        self.boton_siguiente = tk.Button(self.marco_botones, text="⏭️", command=self.cancion_siguiente, bg="#007BFF", fg="#ffffff", font=("Arial", 14), width=3, activebackground="#0056b3")
        self.boton_siguiente.grid(row=0, column=2, padx=5)

        # Inicializar el combobox para "Mostrar por"
        self.combo_mostrar_por = ttk.Combobox(master, state='readonly')
        self.combo_mostrar_por['values'] = ("Artista", "Álbum", "Canción")
        self.combo_mostrar_por.current(0)  # Establecer el valor predeterminado
        self.combo_mostrar_por.pack(pady=5)

        # Menú contextual para ajustes
        self.menu_contextual = tk.Menu(master, tearoff=0)
        self.menu_contextual.add_command(label="Ajustes", command=self.abrir_ajustes)
        self.master.bind("<Button-3>", self.mostrar_menu_contextual)  # Botón derecho del mouse

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

        self.combo_mostrar_por_ajustes = ttk.Combobox(ventana_ajustes, state='readonly')
        self.combo_mostrar_por_ajustes['values'] = ("Artista", "Álbum", "Canción")
        self.combo_mostrar_por_ajustes.current(self.combo_mostrar_por.current())  # Establecer el valor actual
        self.combo_mostrar_por_ajustes.pack(pady=10)

        boton_guardar = tk.Button(ventana_ajustes, text="Guardar", command=lambda: self.guardar_ajustes(ventana_ajustes))
        boton_guardar.pack(pady=10)

    def cargar_ajustes(self):
        # Cargar ajustes desde un archivo JSON, si existe
        if os.path.exists('ajustes.json'):
            with open('ajustes.json', 'r') as archivo:
                ajustes = json.load(archivo)
                self.modo_mostrar_por = ajustes.get("modo_mostrar_por", "Canción")  # Valor por defecto si no se encuentra
                self.combo_mostrar_por.current(("Artista", "Álbum", "Canción").index(self.modo_mostrar_por))

    def guardar_ajustes(self, ventana):
        self.modo_mostrar_por = self.combo_mostrar_por_ajustes.get()
        self.lista.delete(0, tk.END)  # Limpia la lista actual
        self.cargar_mp3()  # Recargar MP3 con el nuevo modo

        # Guardar ajustes en el archivo JSON
        ajustes = {"modo_mostrar_por": self.modo_mostrar_por}
        with open('ajustes.json', 'w') as archivo:
            json.dump(ajustes, archivo)

        ventana.destroy()

    def configurar_evento_finalizacion(self):
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)  # Configura el evento para finalizar

    def cargar_mp3(self):
        directorio = 'files'  # Carpeta estática
        self.archivos_mp3 = []
        self.lista.delete(0, tk.END)  # Limpia la lista existente

        artistas = {}
        albums = {}

        for root, dirs, files in os.walk(directorio):
            for file in files:
                if file.endswith(".mp3"):
                    ruta_completa = os.path.join(root, file)
                    self.archivos_mp3.append(ruta_completa)

                    # Extraer información del archivo MP3
                    try:
                        audio = MP3(ruta_completa)
                        artista = audio.get('TPE1', ["Artista desconocido"])[0]
                        album = audio.get('TALB', ["Álbum desconocido"])[0]
                    except Exception:
                        artista = "Artista desconocido"
                        album = "Álbum desconocido"

                    if self.modo_mostrar_por == "Artista":
                        if artista not in artistas:
                            artistas[artista] = []
                        artistas[artista].append((album, file, ruta_completa))

                    elif self.modo_mostrar_por == "Álbum":
                        if album not in albums:
                            albums[album] = []
                        albums[album].append((file, ruta_completa))
                    
                    else:
                        self.lista.insert(tk.END, file)  # Mostrar como canciones

        # Cargar en la lista dependiendo del modo seleccionado
        if self.modo_mostrar_por == "Artista":
            for artista, albums_info in artistas.items():
                self.lista.insert(tk.END, artista)  # Mostrar artistas
                for album, file, ruta in albums_info:
                    self.lista.insert(tk.END, f"  {album} - {file}")  # Mostrar álbumes y canciones

        elif self.modo_mostrar_por == "Álbum":
            for album, canciones in albums.items():
                self.lista.insert(tk.END, album)  # Mostrar álbumes
                for file, ruta in canciones:
                    self.lista.insert(tk.END, f"  {file}")  # Mostrar canciones

        elif self.modo_mostrar_por == "Canción":
            for file in self.archivos_mp3:
                nombre_archivo = os.path.basename(file)
                self.lista.insert(tk.END, nombre_archivo)  # Mostrar solo canciones

    def reproducir_cancion_seleccionada(self, event):
        seleccion = self.lista.curselection()
        if seleccion:
            index = seleccion[0]
            self.indice_actual = index  # Actualiza el índice actual
            self.archivo_actual = self.archivos_mp3[index]
            pygame.mixer.music.load(self.archivo_actual)
            pygame.mixer.music.play()
            self.actualizar_info_cancion()

    def actualizar_info_cancion(self):
        if self.archivo_actual:
            nombre_archivo = os.path.basename(self.archivo_actual)
            self.titulo_cancion.config(text=nombre_archivo)

            # Extraer y mostrar el artista si se puede
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
            self.indice_actual -= 1  # Disminuir el índice
            self.archivo_actual = self.archivos_mp3[self.indice_actual]  # Obtener la nueva canción
            pygame.mixer.music.load(self.archivo_actual)  # Cargar la nueva canción
            pygame.mixer.music.play()  # Reproducir la nueva canción
            self.lista.selection_clear(0, tk.END)  # Limpiar selección
            self.lista.selection_set(self.indice_actual)  # Seleccionar la nueva canción
            self.lista.activate(self.indice_actual)  # Activar la nueva canción en la lista
            self.actualizar_info_cancion()  # Actualiza la información de la canción

    def cancion_siguiente(self):
        if self.indice_actual < len(self.archivos_mp3) - 1:
            self.indice_actual += 1  # Aumentar el índice
            self.archivo_actual = self.archivos_mp3[self.indice_actual]  # Obtener la nueva canción
            pygame.mixer.music.load(self.archivo_actual)  # Cargar la nueva canción
            pygame.mixer.music.play()  # Reproducir la nueva canción
            self.lista.selection_clear(0, tk.END)  # Limpiar selección
            self.lista.selection_set(self.indice_actual)  # Seleccionar la nueva canción
            self.lista.activate(self.indice_actual)  # Activar la nueva canción en la lista
            self.actualizar_info_cancion()  # Actualiza la información de la canción


if __name__ == "__main__":
    root = tk.Tk()
    app = ReproductorMP3(root)
    root.mainloop()
