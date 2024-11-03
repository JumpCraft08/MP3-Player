import tkinter as tk
from tkinter import Toplevel, messagebox

def abrir_informacion(master):
    ventana_info = Toplevel(master)
    ventana_info.title("Información")
    ventana_info.geometry("350x200")

    tk.Label(ventana_info, text="Reproductor MP3 - Versión 1.0\nDesarrollado por JumpCraft", justify='center').pack(pady=10)
    tk.Button(ventana_info, text="Licencia", command=lambda: mostrar_licencia()).pack(pady=10)

def mostrar_licencia():
    licencia = ("MIT License\n\n"
                "Copyright (c) 2024 JumpCraft\n\n"
                "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
                "of this software and associated documentation files (the \"Software\"), to deal\n"
                "in the Software without restriction, including without limitation the rights\n"
                "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
                "copies of the Software, and to permit persons to whom the Software is\n"
                "furnished to do so, subject to the following conditions:\n\n"
                "The above copyright notice and this permission notice shall be included in all\n"
                "copies or substantial portions of the Software.\n\n"
                "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
                "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
                "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
                "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
                "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
                "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
                "SOFTWARE.")

    messagebox.showinfo("Licencia", licencia)
