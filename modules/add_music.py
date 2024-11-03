import os
import shutil
from mutagen.mp3 import MP3
from tkinter import filedialog, messagebox

def añadir_musica(cargar_mp3_callback):
    # Abrir un diálogo para seleccionar un archivo de música
    ruta_archivo = filedialog.askopenfilename(title="Seleccionar archivo MP3", filetypes=[("Archivos MP3", "*.mp3")])
    if not ruta_archivo:
        return

    # Extraer metadatos
    try:
        audio = MP3(ruta_archivo)
        artista = audio.get('TPE1', ["Desconocido"])[0]
        album = audio.get('TALB', ["Desconocido"])[0]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron leer los metadatos: {e}")
        return

    # Crear la estructura de carpetas
    carpeta_artista = os.path.join("files", artista)
    carpeta_album = os.path.join(carpeta_artista, album)

    os.makedirs(carpeta_album, exist_ok=True)

    # Mover el archivo a la carpeta correspondiente
    nombre_archivo = os.path.basename(ruta_archivo)
    destino = os.path.join(carpeta_album, nombre_archivo)

    shutil.copy(ruta_archivo, destino)
    messagebox.showinfo("Éxito", "La música se ha añadido correctamente.")
    
    # Actualizar la lista de canciones
    cargar_mp3_callback()  # Llamar a la función para cargar las canciones
