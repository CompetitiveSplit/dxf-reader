import sys
import ezdxf
import math
import os
from tkinter import Tk, Label, Button, filedialog, Entry, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

class DXFAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("DXF Reader")
        self.root.geometry("800x600")
        self.root.style = ttk.Style()
        self.root.style.theme_use("ubuntu")

        self.label = Label(root, text="Archivo DXF:")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry = Entry(root, width=40)
        self.entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.browse_button = Button(root, text="Buscar DXF", command=self.browse_dxf)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.analyze_button = Button(root, text="Analizar DXF", command=self.analyze_dxf)
        self.analyze_button.grid(row=1, column=0, columnspan=3, pady=10)

        self.total_length_label = Label(root, text="Longitud total:")
        self.total_length_label.grid(row=2, column=0, columnspan=3, pady=10)

        self.tree = ttk.Treeview(root, columns=("Start X", "Start Y", "End X", "End Y", "Length"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Start X", text="Start X")
        self.tree.heading("Start Y", text="Start Y")
        self.tree.heading("End X", text="End X")
        self.tree.heading("End Y", text="End Y")
        self.tree.heading("Length", text="Length")
        self.tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(0, weight=1)

    def browse_dxf(self):
        file_path = filedialog.askopenfilename(filetypes=[("DXF files", "*.dxf")])
        if file_path:
            self.entry.delete(0, "end")
            self.entry.insert(0, file_path)

    def analyze_dxf(self):
        file_path = self.entry.get()
        if not file_path:
            messagebox.showerror("Error", "Por favor, selecciona un archivo DXF.")
            return

        try:
            my_file = ezdxf.readfile(file_path)
            msp = my_file.modelspace()
            total_length = 0

            for item in self.tree.get_children():
                self.tree.delete(item)

            for i, e in enumerate(msp.query("LINE")):
                length = self.get_length(e.dxf.start, e.dxf.end)
                total_length += length
                self.print_entity(e, i + 1, length)

            self.total_length_label.config(text=f"Longitud total: {total_length}")

        except IOError:
            messagebox.showerror("Error", "No es un archivo DXF o un error de E/S genérico.")
        except ezdxf.DXFStructureError:
            messagebox.showerror("Error", "Archivo DXF inválido o corrupto.")

    def print_entity(self, e, index, length):
        start_x, start_y = e.dxf.start.x, e.dxf.start.y
        end_x, end_y = e.dxf.end.x, e.dxf.end.y

        self.tree.insert("", "end", text=index, values=(start_x, start_y, end_x, end_y, length))

    def get_length(self, start, end):
        return math.sqrt((end.x - start.x)**2 + (end.y - start.y)**2)

    @staticmethod
    def get_length(start, end):
        return math.dist(start, end)

if __name__ == "__main__":
    root = Tk()
    app = DXFAnalyzer(root)
    root.mainloop()
