import tkinter as tk
from tkinter import ttk, Scrollbar

def create_widgets(root, select_song, previous_song, toggle_play_pause, next_song):
    title_label = tk.Label(root, text="Biblioteca de Música", font=("Arial", 20, "bold"), bg="#2C3E50", fg="#ECF0F1")
    title_label.pack(pady=10)

    tree_frame = tk.Frame(root, bg="#2C3E50")
    tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(tree_frame)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tree_scroll = Scrollbar(tree_frame, command=tree.yview)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    tree.config(yscrollcommand=tree_scroll.set)

    tree["columns"] = ("name", "path")
    tree.column("#0", width=300, anchor="w")
    tree.column("name", width=100, anchor="w")
    tree.column("path", width=200, anchor="w")
    tree.heading("#0", text="Biblioteca de Música", anchor="w")
    tree.heading("name", text="Nombre")
    tree.heading("path", text="Ruta")
    tree.bind("<Double-1>", select_song)

    # Frame para la información de la canción y controles
    info_frame = tk.Frame(root, bg="#2C3E50")
    info_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)

    # Etiqueta de imagen de álbum
    album_art = tk.Label(info_frame, bg="#2C3E50")
    album_art.grid(row=0, column=0, rowspan=2, padx=10, pady=5)

    # Etiqueta de nombre de canción
    song_label = tk.Label(info_frame, text="No hay canción en reproducción", font=("Arial", 14), fg="white", bg="#2C3E50")
    song_label.grid(row=0, column=1, sticky="w")

    # Etiqueta para mostrar el álbum
    album_name_label = tk.Label(info_frame, text="Álbum: Desconocido", font=("Arial", 12), fg="#BDC3C7", bg="#2C3E50")
    album_name_label.grid(row=1, column=1, sticky="w")

    # Botones de control
    frame_controls = tk.Frame(info_frame, bg="#2C3E50")
    frame_controls.grid(row=0, column=2, rowspan=2, sticky="e", padx=10)

    prev_button = tk.Button(frame_controls, text="⏮", command=previous_song, bg="#2C3E50", fg="white", font=("Arial", 20), borderwidth=0, activebackground="#2C3E50")
    prev_button.grid(row=0, column=0, padx=5)

    play_pause_button = tk.Button(frame_controls, text="▶️", command=toggle_play_pause, bg="#2C3E50", fg="white", font=("Arial", 20), borderwidth=0, activebackground="#2C3E50")
    play_pause_button.grid(row=0, column=1, padx=5)

    next_button = tk.Button(frame_controls, text="⏭", command=next_song, bg="#2C3E50", fg="white", font=("Arial", 20), borderwidth=0, activebackground="#2C3E50")
    next_button.grid(row=0, column=2, padx=5)

    # Barra de progreso
    progress_frame = tk.Frame(root, bg="#00BFFF", height=10)  # Color azul claro
    progress_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # Círculo de progreso
    circle_radius = 10
    circle = tk.Canvas(progress_frame, width=800, height=10)
    circle.pack(fill=tk.X)

    # Dibuja el círculo en la posición inicial
    circle_indicator = circle.create_oval(0, 0, circle_radius * 2, circle_radius * 2, fill="#34495E", outline="")

    return {
        "tree": tree,
        "album_art": album_art,
        "song_label": song_label,
        "play_pause_button": play_pause_button,
        "album_name_label": album_name_label,
        "progress_frame": progress_frame,
        "circle": circle,
        "circle_indicator": circle_indicator,
        "circle_radius": circle_radius,
    }
