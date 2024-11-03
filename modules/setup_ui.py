import tkinter as tk
from modules.license import abrir_informacion

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
