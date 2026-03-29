import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import os, shutil, subprocess
import file_operations as fo
from folder_operations import create_folder, delete_folder
from history import log_action, read_history, reset_history

class FileManagerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Archivos")
        self.root.geometry("500x650")
        self.folder_path = None

        # seleccionar carpeta
        self.select_button = tk.Button(
            root,
            text="Seleccionar carpeta",
            command=self.select_folder
        )
        self.select_button.pack(pady=10)

        self.path_label = tk.Label(root, text="")

        self.create_folder_button = tk.Button(
            root,
            text="Crear subcarpeta",
            command=self.create_subfolder
        )

        self.create_file_button = tk.Button(
            root,
            text="Crear archivo",
            command=self.create_file
        )

        self.open_file_button = tk.Button(
            root,
            text="Abrir archivo",
            command=self.open_file_action
        )

        self.copy_file_button = tk.Button(
            root,
            text="Copiar archivo",
            command=self.copy_file_action
        )

        self.delete_file_button = tk.Button(
            root,
            text="Eliminar archivo",
            command=self.delete_file_action
        )
        
        self.delete_folder_button = tk.Button(
            root,
            text="Eliminar carpeta",
            command=self.delete_folder_action
        )
        
        self.rename_file_button = tk.Button(
            root,
            text="Renombrar archivo",
            command=self.rename_action
        )

        self.rename_button_folder = tk.Button(
            root,
            text="Renombrar carpeta",
            command=self.rename_folder_action
        )

        self.progress = ttk.Progressbar(
            root,
            orient="horizontal",
            length=300,
            mode="determinate"
        ) # No sirve

        self.history_button = tk.Button(
            root,
            text="Ver historial",
            command=self.show_history
        )

        self.progress.pack(pady=10)

    # seleccionar carpeta
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
        self.copy_file_button.pack(pady=5)
        self.delete_file_button.pack(pady=5)
        self.delete_folder_button.pack(pady=5)
        self.rename_file_button.pack(pady=5)
        self.rename_button_folder.pack(pady=5)
        self.history_button.pack(pady=5)

    # crear carpeta
    def create_subfolder(self):
        folder_name = simpledialog.askstring(
            "Crear Carpeta",
            "Nombre de la nueva carpeta:"
        )
        if folder_name:
            new_folder_path = create_folder(self.folder_path, folder_name)
            messagebox.showinfo("Éxito", f"Carpeta creada: {new_folder_path}")

    # crear archivo
    def create_file(self):
        file_name = simpledialog.askstring(
            "Crear Archivo",
            "Nombre del archivo:"
        )
        if not file_name:
            return

        if '.' not in file_name:
            file_name += ".txt"

        file_path = os.path.join(self.folder_path, file_name)
        base, ext = os.path.splitext(file_name)
        counter = 1

        while os.path.exists(file_path):
            file_path = os.path.join(self.folder_path, f"{base}({counter}){ext}")
            counter += 1

        with open(file_path, 'w') as f:
            f.write("")

        log_action(f"Archivo creado: {file_path}")
        messagebox.showinfo("Éxito", f"Archivo creado: {file_path}")

    # abrir archivo
    def open_file_action(self):
        file_path = filedialog.askopenfilename(
            initialdir=self.folder_path,
            title="Selecciona archivo"
        )
        if not file_path:
            return
        os.startfile(file_path)

    # copiar archivos
    def copy_file_action(self):
        files = filedialog.askopenfilenames(
            initialdir=self.folder_path,
            title="Selecciona archivos a copiar"
        )
        if not files:
            return

        destination = filedialog.askdirectory(title="Selecciona carpeta destino")
        if not destination:
            return

        self.progress["maximum"] = len(files)
        copied = 0

        for i, file in enumerate(files):
            try:
                filename = os.path.basename(file)
                base, ext = os.path.splitext(filename)
                destination_path = os.path.join(destination, filename)
                counter = 1

                while os.path.exists(destination_path):
                    destination_path = os.path.join(destination, f"{base}({counter}){ext}")
                    counter += 1

                shutil.copy2(file, destination_path)
                log_action(f"Archivo copiado: {file} -> {destination_path}")
                copied += 1

            except Exception as e:
                messagebox.showerror("Error", str(e))

            self.progress["value"] = i + 1
            self.root.update_idletasks()

        messagebox.showinfo("Éxito", f"{copied} archivos copiados")
        self.progress["value"] = 0
        
    # Eliminar archivos
    def delete_file_action(self):
        
        files = filedialog.askopenfilenames(
            initialdir=self.folder_path,
            title="Selecciona archivos a eliminar"
        )

        if not files:
            return

        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Seguro que quieres eliminar {len(files)} archivo(s)?"
        )

        if not confirm:
            return

        deleted = 0

        for file in files:
            try:
                os.remove(file)
                log_action(f"Archivo eliminado: {file}")
                deleted += 1
            except Exception as e:
                messagebox.showerror("Error", str(e))

        messagebox.showinfo("Resultado", f"{deleted} archivo(s) eliminado(s)")

    # eliminar archivos o carpetas (individual o múltiple)
    def delete_folder_action(self):

        folders = []

        while True:

            folder = filedialog.askdirectory(
                initialdir=self.folder_path,
                title="Selecciona una carpeta"
            )

            if not folder:
                break

            folders.append(folder)

            another = messagebox.askyesno(
                "Añadir otra carpeta",
                "¿Quieres seleccionar otra carpeta?"
            )

            if not another:
                break

        if not folders:
            return

        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Seguro que quieres eliminar {len(folders)} carpeta(s)?"
        )

        if not confirm:
            return

        deleted = 0

        for folder in folders:
            try:
                shutil.rmtree(folder)
                log_action(f"Carpeta eliminada: {folder}")
                deleted += 1
            except Exception as e:
                messagebox.showerror("Error", str(e))

        messagebox.showinfo("Resultado", f"{deleted} carpeta(s) eliminada(s)")
    
    # renombrar archivo
    def rename_action(self):
        files = filedialog.askopenfilenames(
            initialdir=self.folder_path,
            title="Selecciona archivos a renombrar"
        )

        if not files:
            return

        for file in files:

            old_name = os.path.basename(file)

            new_name = simpledialog.askstring(
                "Renombrar archivo",
                f"Nuevo nombre para:\n{old_name}"
            )

            if not new_name:
                continue

            base, ext = os.path.splitext(old_name)

            # mantener extensión si el usuario no la pone
            if "." not in new_name:
                new_name += ext

            new_path = os.path.join(os.path.dirname(file), new_name)

            try:
                os.rename(file, new_path)
                log_action(f"Archivo renombrado: {file} -> {new_path}")

            except Exception as e:
                messagebox.showerror("Error", str(e))

        messagebox.showinfo("Éxito", "Renombrado completado")

    # renombrar carpeta
    def rename_folder_action(self):
        folder = filedialog.askdirectory(
            initialdir=self.folder_path,
            title="Selecciona carpeta a renombrar"
        )

        if not folder:
            return

        old_name = os.path.basename(folder)
        new_name = simpledialog.askstring(
            "Renombrar carpeta",
            f"Nuevo nombre para:\n{old_name}"
        )

        if not new_name:
            return

        new_path = os.path.join(os.path.dirname(folder), new_name)

        try:
            os.rename(folder, new_path)
            log_action(f"Carpeta renombrada: {folder} -> {new_path}")
            messagebox.showinfo("Éxito", f"Carpeta renombrada a: {new_name}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # mostrar historial
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Historial de acciones")
        history_window.geometry("500x400")

        frame = tk.Frame(history_window)
        frame.pack(expand=True, fill="both")

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text_area = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set)
        text_area.pack(side="left", expand=True, fill="both")
        scrollbar.config(command=text_area.yview)

        history_data = read_history()
        text_area.insert("1.0", history_data)
        text_area.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
    reset_history()  # reinicia historial