import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os, shutil
from folder_operations import create_folder
from history import log_action, read_history, reset_history

class FileManagerApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Gestor de Archivos")
        self.root.geometry("500x650")

        self.folder_path = None

        # botón seleccionar carpeta
        self.select_button = tk.Button(
            root,
            text="Seleccionar carpeta",
            command=self.select_folder
        )
        self.select_button.pack(pady=10)

        # etiqueta ruta actual
        self.path_label = tk.Label(root, text="")

        # botones
        self.create_folder_button = tk.Button(root, text="Crear subcarpeta", command=self.create_subfolder)
        self.create_file_button = tk.Button(root, text="Crear archivo", command=self.create_file)
        self.open_file_button = tk.Button(root, text="Abrir archivo", command=self.open_file_action)
        self.copy_file_button = tk.Button(root, text="Copiar archivo", command=self.copy_file_action)
        self.delete_file_button = tk.Button(root, text="Eliminar archivo", command=self.delete_file_action)
        self.delete_folder_button = tk.Button(root, text="Eliminar carpeta", command=self.delete_folder_action)
        self.rename_file_button = tk.Button(root, text="Renombrar archivo", command=self.rename_action)
        self.rename_folder_button = tk.Button(root, text="Renombrar carpeta", command=self.rename_folder_action)

        # botón reportar historial
        self.report_history_button = tk.Button(root, text="Reportar historial", command=self.export_history)

        # consola historial estilo CMD (invisible hasta seleccionar carpeta)
        self.history_console = tk.Text(
            root,
            height=12,
            bg="#0c0c0c",
            fg="#cccccc",
            font=("Consolas", 10),
            insertbackground="white"
        )

        # colores por tipo de acción
        self.history_console.tag_config("create", foreground="cyan")
        self.history_console.tag_config("copy", foreground="yellow")
        self.history_console.tag_config("delete", foreground="red")
        self.history_console.tag_config("rename", foreground="lime")
        self.history_console.tag_config("normal", foreground="white")

        self.history_console.config(state="disabled")

    # seleccionar carpeta
    def select_folder(self):
        folder = filedialog.askdirectory(title="Selecciona la carpeta")
        if not folder:
            return

        self.folder_path = folder

        self.path_label.config(text=f"Carpeta actual: {folder}")
        self.path_label.pack(pady=5)

        # mostrar botones
        self.create_folder_button.pack(pady=5)
        self.create_file_button.pack(pady=5)
        self.open_file_button.pack(pady=5)
        self.copy_file_button.pack(pady=5)
        self.delete_file_button.pack(pady=5)
        self.delete_folder_button.pack(pady=5)
        self.rename_file_button.pack(pady=5)
        self.rename_folder_button.pack(pady=5)
        self.report_history_button.pack(pady=5)

        # mostrar consola historial abajo
        self.history_console.pack(pady=10, fill="both", expand=True)
        self.update_history_console()

    # crear subcarpeta
    def create_subfolder(self):
        name = simpledialog.askstring("Crear carpeta", "Nombre de la carpeta:")
        if not name:
            return

        path = create_folder(self.folder_path, name)
        log_action(f"Carpeta creada: {path}")
        self.update_history_console()
        messagebox.showinfo("Éxito", f"Carpeta creada: {path}")

    # crear archivo
    def create_file(self):
        name = simpledialog.askstring("Crear archivo", "Nombre del archivo:")
        if not name:
            return

        if "." not in name:
            name += ".txt"

        path = os.path.join(self.folder_path, name)
        base, ext = os.path.splitext(name)
        counter = 1
        while os.path.exists(path):
            path = os.path.join(self.folder_path, f"{base}({counter}){ext}")
            counter += 1

        with open(path, "w") as f:
            f.write("")

        log_action(f"Archivo creado: {path}")
        self.update_history_console()
        messagebox.showinfo("Éxito", f"Archivo creado: {path}")

    # abrir archivo
    def open_file_action(self):
        file = filedialog.askopenfilename(initialdir=self.folder_path)
        if file:
            os.startfile(file)

    # copiar archivos
    def copy_file_action(self):
        files = filedialog.askopenfilenames(initialdir=self.folder_path)
        if not files:
            return

        destination = filedialog.askdirectory()
        if not destination:
            return

        for file in files:
            name = os.path.basename(file)
            base, ext = os.path.splitext(name)
            dest = os.path.join(destination, name)
            counter = 1
            while os.path.exists(dest):
                dest = os.path.join(destination, f"{base}({counter}){ext}")
                counter += 1
            shutil.copy2(file, dest)
            log_action(f"Archivo copiado: {file} -> {dest}")

        self.update_history_console()
        messagebox.showinfo("Éxito", "Archivos copiados")

    # eliminar archivos
    def delete_file_action(self):
        files = filedialog.askopenfilenames(initialdir=self.folder_path)
        if not files:
            return

        confirm = messagebox.askyesno("Confirmar", f"Eliminar {len(files)} archivos?")
        if not confirm:
            return

        for file in files:
            os.remove(file)
            log_action(f"Archivo eliminado: {file}")

        self.update_history_console()
        messagebox.showinfo("Resultado", "Archivos eliminados")

    # eliminar carpeta
    def delete_folder_action(self):
        folder = filedialog.askdirectory(initialdir=self.folder_path)
        if not folder:
            return

        confirm = messagebox.askyesno("Confirmar", f"Eliminar carpeta?\n{folder}")
        if not confirm:
            return

        shutil.rmtree(folder)
        log_action(f"Carpeta eliminada: {folder}")
        self.update_history_console()

    # renombrar archivo
    def rename_action(self):
        files = filedialog.askopenfilenames(initialdir=self.folder_path)
        if not files:
            return

        for file in files:
            old = os.path.basename(file)
            new = simpledialog.askstring("Renombrar archivo", f"Nuevo nombre para:\n{old}")
            if not new:
                continue
            base, ext = os.path.splitext(old)
            if "." not in new:
                new += ext
            new_path = os.path.join(os.path.dirname(file), new)
            os.rename(file, new_path)
            log_action(f"Archivo renombrado: {file} -> {new_path}")

        self.update_history_console()
        messagebox.showinfo("Éxito", "Renombrado completado")

    # renombrar carpeta
    def rename_folder_action(self):
        folder = filedialog.askdirectory(initialdir=self.folder_path)
        if not folder:
            return

        old = os.path.basename(folder)
        new = simpledialog.askstring("Renombrar carpeta", f"Nuevo nombre para:\n{old}")
        if not new:
            return

        new_path = os.path.join(os.path.dirname(folder), new)
        os.rename(folder, new_path)
        log_action(f"Carpeta renombrada: {folder} -> {new_path}")
        self.update_history_console()

    # actualizar consola historial
    def update_history_console(self):
        self.history_console.config(state="normal")
        self.history_console.delete("1.0", tk.END)
        history = read_history().split("\n")
        for line in history:
            if "creada" in line.lower() or "creado" in line.lower():
                tag = "create"
            elif "copiado" in line.lower():
                tag = "copy"
            elif "eliminado" in line.lower():
                tag = "delete"
            elif "renombrado" in line.lower():
                tag = "rename"
            else:
                tag = "normal"
            self.history_console.insert(tk.END, line + "\n", tag)
        self.history_console.config(state="disabled")
        self.history_console.see(tk.END)

    # exportar historial a archivo
    def export_history(self):
        history = read_history()
        if not history.strip():
            messagebox.showwarning("Aviso", "No hay historial para exportar")
            return

        file_path = filedialog.asksaveasfilename(
            title="Guardar reporte de historial",
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt")]
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("REPORTE DE HISTORIAL\n")
                f.write("=====================\n\n")
                f.write(history)

            messagebox.showinfo("Éxito", f"Historial exportado en:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
    reset_history()  # reinicia historial al cerrar la app