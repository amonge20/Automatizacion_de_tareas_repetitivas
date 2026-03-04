import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import file_operations as fo
from folder_operations import create_folder, delete_folder
import subprocess

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

        self.open_file_button = tk.Button(
            root, text="Abrir archivo", command=self.open_file_action
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
            root, text="Renombrar archivo", command=self.rename_action
        )

        self.rename_button_folder = tk.Button(
            root, text="Renombrar carpeta", command=self.rename_folder_action
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
        self.open_file_button.pack(pady=5)
        self.delete_folder_button.pack(pady=5)
        self.delete_file_button.pack(pady=5)
        self.organize_button.pack(pady=5)
        self.rename_button.pack(pady=5)
        self.rename_button_folder.pack(pady=5)
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
            "Crear Archivo", "Nombre del archivo:")
        if not file_name:
            return  # Usuario canceló

        # Si no se especifica extensión, añadimos .txt por defecto
        if '.' not in file_name:
            file_name += ".txt"

        file_path = os.path.join(self.folder_path, file_name)

        # Si el archivo ya existe, añadir sufijo numérico
        base, ext = os.path.splitext(file_name)
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(self.folder_path, f"{base}({counter}){ext}")
            counter += 1

        # Crear archivo vacío
        with open(file_path, 'w') as f:
            f.write("")

        messagebox.showinfo("Éxito", f"Archivo creado: {file_path}")
    
    def open_file_action(self):
        if not self.folder_path:
            messagebox.showwarning("Aviso", "No hay carpeta seleccionada")
            return

        # Selecciona un archivo
        file_path = filedialog.askopenfilename(
            initialdir=self.folder_path,
            title="Selecciona un archivo para abrir"
        )

        if not file_path:
            return  # Canceló

        try:
            # Abrir con la aplicación por defecto del sistema operativo
            if os.name == "nt":  # Windows
                os.startfile(file_path)
            elif os.name == "posix":  # macOS / Linux
                subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", file_path])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{str(e)}")


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
        if not self.folder_path:
            messagebox.showwarning("Aviso", "No hay carpeta seleccionada.")
            return

        # Seleccionar archivo
        selected_path = filedialog.askopenfilename(
            initialdir=self.folder_path,
            title="Selecciona un archivo para renombrar"
        )

        if not selected_path:
            messagebox.showerror("Error", "No se ha seleccionado ningún archivo")
            return

        old_name = os.path.basename(selected_path)
        old_base, old_ext = os.path.splitext(old_name)

        # Pedir nuevo nombre
        new_name = simpledialog.askstring(
            "Renombrar",
            "Introduce el nuevo nombre:",
            initialvalue=old_name
        )

        if new_name is None:
            messagebox.showerror("Error", "No se ha especificado un nuevo nombre.")
            return

        new_name = new_name.strip()

        if not new_name:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return

        new_base, new_ext = os.path.splitext(new_name)

        # 🔹 Si el usuario no pone extensión
        if not new_ext:
            if old_ext:
                # Mantener la extensión original
                new_name = new_name + old_ext
            else:
                # Si el original tampoco tenía extensión → poner .txt
                new_name = new_name + ".txt"

        # Si el nombre final es el mismo
        if new_name == old_name:
            messagebox.showwarning("Aviso", "No se pudo cambiar el nombre porque es el mismo.")
            return

        new_path = os.path.join(os.path.dirname(selected_path), new_name)

        if os.path.exists(new_path):
            messagebox.showerror("Error", "Ya existe un archivo con ese nombre.")
            return

        try:
            os.rename(selected_path, new_path)

            messagebox.showinfo(
                "Éxito",
                f"Se ha cambiado el nombre del archivo de '{old_name}' a '{new_name}'."
            )

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cambiar el nombre:\n{str(e)}")

    # Para cambiar el nombre de la carpeta
    def rename_folder_action(self):
        if not self.folder_path:
            messagebox.showwarning("Aviso", "No hay carpeta seleccionada.")
            return

        # Seleccionar carpeta a renombrar
        selected_path = filedialog.askdirectory(
            initialdir=self.folder_path,
            title="Selecciona una carpeta para renombrar"
        )

        # Si cancela selección
        if not selected_path:
            messagebox.showerror("Error", "No se ha seleccionado ninguna carpeta.")
            return

        old_name = os.path.basename(selected_path)

        # Pedir nuevo nombre
        new_name = simpledialog.askstring(
            "Renombrar carpeta",
            "Introduce el nuevo nombre:",
            initialvalue=old_name
        )

        # Si cancela el nuevo nombre
        if new_name is None:
            messagebox.showerror("Error", "No se ha especificado un nuevo nombre.")
            return

        new_name = new_name.strip()

        if not new_name:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return

        # Si el nombre es el mismo
        if new_name == old_name:
            messagebox.showwarning("Aviso", "No se pudo cambiar el nombre porque es el mismo.")
            return

        new_path = os.path.join(os.path.dirname(selected_path), new_name)

        # Si ya existe carpeta con ese nombre
        if os.path.exists(new_path):
            messagebox.showerror("Error", "Ya existe una carpeta con ese nombre.")
            return

        try:
            os.rename(selected_path, new_path)

            messagebox.showinfo(
                "Éxito",
                f"Se ha cambiado el nombre de la carpeta de '{old_name}' a '{new_name}'."
            )

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cambiar el nombre:\n{str(e)}")

    # Eliminar duplicados
    def delete_action(self):
        fo.delete_duplicates(self.folder_path)
        messagebox.showinfo("Éxito", "Duplicados eliminados")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()