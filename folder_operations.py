import os
import shutil
from tkinter import messagebox
from history import log_action

def create_folder(parent_folder, new_folder_name):
    folder_path = os.path.join(parent_folder, new_folder_name)
    os.makedirs(folder_path, exist_ok=True)
    log_action(f"Carpeta creada: {folder_path}")
    return folder_path


def delete_folder(folder_path):
    if not os.path.exists(folder_path):
        messagebox.showwarning("Advertencia", "La carpeta no existe")
        return False

    confirm = messagebox.askyesno(
        "Confirmar eliminación",
        f"¿Estás seguro de eliminar la carpeta?\n{folder_path}\nEsto eliminará todo su contenido."
    )

    if confirm:
        try:
            shutil.rmtree(folder_path)
            log_action(f"Carpeta eliminada: {folder_path}")
            messagebox.showinfo("Éxito", f"Carpeta eliminada: {folder_path}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la carpeta:\n{str(e)}")
            return False
    return False