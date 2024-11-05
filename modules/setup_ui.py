import tkinter as tk
from tkinter import ttk, Toplevel
from modules.license import abrir_informacion

def setup_ui(self):
    # Código de configuración de la UI (sin cambios)
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

    # Marco inferior con controles
    self.marco_bajo = tk.Frame(self.master, bg="#3e444f")
    self.marco_bajo.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(10, 10))

    # Marco para los textos de la canción
    self.marco_textos = tk.Frame(self.marco_bajo, bg="#3e444f")
    self.marco_textos.pack(side=tk.LEFT, padx=10, pady=10)

    self.titulo_cancion = tk.Label(self.marco_textos, text="No hay canción sonando", bg="#3e444f", fg="#ffffff", font=("Arial", 14, "bold"), anchor='w')
    self.titulo_cancion.pack(side=tk.TOP, fill=tk.X)

    self.artista_cancion = tk.Label(self.marco_textos, text="", bg="#3e444f", fg="#a9a9a9", font=("Arial", 12))
    self.artista_cancion.pack(side=tk.TOP)

    # Marco para los botones de control
    self.marco_botones = tk.Frame(self.marco_bajo, bg="#3e444f")
    self.marco_botones.pack(side=tk.RIGHT, padx=10)

    self.boton_anterior = self.crear_boton(self.marco_botones, "⏮️", lambda: self.cambiar_cancion(-1))
    self.boton_pausa_reproducir = self.crear_boton(self.marco_botones, "▶️", self.pausar_reproducir)
    self.boton_siguiente = self.crear_boton(self.marco_botones, "⏭️", lambda: self.cambiar_cancion(1))

    # Contenedor para el slider
    self.marco_slider = tk.Frame(self.marco_bajo, bg="#3e444f")
    self.marco_slider.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 5), padx=10)

    # Tiempo actual y total encima del slider
    self.marco_tiempos = tk.Frame(self.marco_slider, bg="#3e444f")
    self.marco_tiempos.pack(side=tk.TOP, fill=tk.X)

    self.tiempo_actual_label = tk.Label(self.marco_tiempos, text="00:00", bg="#3e444f", fg="#ffffff", font=("Arial", 10))
    self.tiempo_actual_label.pack(side=tk.LEFT)

    # Slider para controlar el tiempo de la canción
    self.slider = tk.Scale(self.marco_slider, from_=0, to=100, orient="horizontal", bg="#3e444f", fg="#ffffff", showvalue=0, sliderlength=20, length=250)
    self.slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
    self.slider.bind("<ButtonRelease-1>", self.mover_slider)

    # Tiempo total
    self.tiempo_total_label = tk.Label(self.marco_tiempos, text="00:00", bg="#3e444f", fg="#ffffff", font=("Arial", 10))
    self.tiempo_total_label.pack(side=tk.RIGHT)

    # Menú contextual
    self.menu_contextual = tk.Menu(self.master, tearoff=0)
    self.menu_contextual.add_command(label="Ajustes", command=lambda: self.abrir_ajustes())
    self.menu_contextual.add_command(label="Añadir música", command=self.añadir_musica)
    self.menu_contextual.add_command(label="Información", command=lambda: abrir_informacion(self.master))
    self.master.bind("<Button-3>", self.mostrar_menu_contextual)

def abrir_ajustes(self):
    ventana_ajustes = Toplevel(self.master)
    ventana_ajustes.title("Ajustes")
    ventana_ajustes.geometry("300x200")

    tk.Label(ventana_ajustes, text="Mostrar por:").pack(pady=10)
    self.combo_mostrar_por_ajustes = ttk.Combobox(ventana_ajustes, state='readonly', values=["Canción"])
    self.combo_mostrar_por_ajustes.current(0)
    self.combo_mostrar_por_ajustes.pack(pady=10)

    tk.Button(ventana_ajustes, text="Guardar", command=lambda: self.guardar_ajustes(ventana_ajustes)).pack(pady=10)
