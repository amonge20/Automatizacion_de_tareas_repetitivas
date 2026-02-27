import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import file_operations as fo
from folder_operations import create_folder, delete_folder


class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Archivos")
        self.root.geometry("500x600")

        self.folder_path = None

        # === BOTÓN SELECCIONAR CARPETA ===
        self.select_button = tk.Button(
            root, text="Seleccionar carpeta", command=self.select_folder
        )
        self.select_button.pack(pady=10)

        # === LABEL RUTA ===
        self.path_label = tk.Label(root, text="")

        # === BOTONES (invisibles al inicio) ===
        self.create_folder_button = tk.Button(
            root, text="Crear subcarpeta", command=self.create_subfolder
        )

        self.create_file_button = tk.Button(
            root, text="Crear archivo", command=self.create_file
        )

        self.delete_folder_button = tk.Button(
            root, text="Eliminar carpeta", command=self.delete_selected_folder
        )

        self.delete_file_button = tk.Button(
            root, text="Eliminar fichero", command=self.delete_file_action
        )

        self.organize_button = tk.Button(
            root, text="Organizar archivos", command=self.organize_action
        )

        self.rename_button = tk.Button(
            root, text="Renombrar archivos", command=self.rename_action
        )

        self.delete_button = tk.Button(
            root, text="Eliminar duplicados", command=self.delete_action
        )

    # ==================================================
    # SELECCIONAR CARPETA
    # ==================================================
    def select_folder(self):
        folder = filedialog.askdirectory(title="Selecciona la carpeta")

        if not folder:
            messagebox.showwarning("Aviso", "No se seleccionó ninguna carpeta")
            return

        self.folder_path = folder

        self.path_label.config(text=f"Carpeta actual: {self.folder_path}")
        self.path_label.pack(pady=5)

        self.create_folder_button.pack(pady=5)
        self.create_file_button.pack(pady=5)
        self.delete_folder_button.pack(pady=5)
        self.delete_file_button.pack(pady=5)
        self.organize_button.pack(pady=5)
        self.rename_button.pack(pady=5)
        self.delete_button.pack(pady=5)

    # ==================================================
    # FUNCIONES
    # ==================================================

    def create_subfolder(self):
        folder_name = simpledialog.askstring(
            "Crear Carpeta", "Nombre de la nueva carpeta:"
        )
        if folder_name:
            new_folder_path = create_folder(self.folder_path, folder_name)
            messagebox.showinfo("Éxito", f"Carpeta creada: {new_folder_path}")

    def create_file(self):
        file_name = simpledialog.askstring(
            "Crear Archivo", "Nombre del archivo:"
        )
        if file_name:
            file_path = os.path.join(self.folder_path, file_name)

            base, ext = os.path.splitext(file_name)
            counter = 1
            while os.path.exists(file_path):
                file_path = os.path.join(
                    self.folder_path, f"{base}({counter}){ext}"
                )
                counter += 1

            with open(file_path, "w") as f:
                f.write("")

            messagebox.showinfo("Éxito", f"Archivo creado: {file_path}")

    def delete_selected_folder(self):
        folder_to_delete = filedialog.askdirectory(
            title="Selecciona la carpeta a eliminar"
        )
        if folder_to_delete:
            delete_folder(folder_to_delete)

    def delete_file_action(self):
        fo.delete_file(self.folder_path)

    # ORGANIZAR ARCHIVOS
    def organize_action(self):
        if not self.folder_path:
            return

        result = fo.organize_files(self.folder_path)

        if result:
            messagebox.showinfo("Éxito", "Archivos organizados correctamente")
        else:
            messagebox.showwarning("Cancelado", "No se movió ningún archivo")

    def rename_action(self):
        fo.rename_files(self.folder_path)
        messagebox.showinfo("Éxito", "Archivos renombrados correctamente")

    def delete_action(self):
        fo.delete_duplicates(self.folder_path)
        messagebox.showinfo("Éxito", "Duplicados eliminados")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()