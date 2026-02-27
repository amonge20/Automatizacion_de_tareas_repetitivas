import os
import shutil
import hashlib
from folder_operations import create_folder
from tkinter import filedialog, messagebox


# --------------------------------------------------
# AUXILIAR: HASH DE ARCHIVO
# --------------------------------------------------
def file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


# --------------------------------------------------
# ORGANIZAR ARCHIVOS (SELECCIÓN INDIVIDUAL/MULTIPLE)
# --------------------------------------------------
def organize_files(folder):
    selected_files = filedialog.askopenfilenames(
        initialdir=folder,
        title="Selecciona uno o varios archivos"
    )

    if not selected_files:
        return False  # Canceló selección

    destination = filedialog.askdirectory(title="Selecciona la carpeta destino")
    if not destination:
        return False  # Canceló destino

    moved = 0

    for file_path in selected_files:
        try:
            filename = os.path.basename(file_path)
            destination_path = os.path.join(destination, filename)

            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(destination_path):
                destination_path = os.path.join(destination, f"{base}({counter}){ext}")
                counter += 1

            shutil.move(file_path, destination_path)
            moved += 1

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mover: {filename}\n{str(e)}")
            continue

    # Devuelve True solo si movió al menos un archivo
    return moved > 0


# --------------------------------------------------
# RENOMBRAR ARCHIVOS
# --------------------------------------------------
def rename_files(folder):
    counter = 1
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            name, ext = os.path.splitext(filename)
            new_name = f"archivo_{counter}{ext}"
            os.rename(file_path, os.path.join(folder, new_name))
            counter += 1


# --------------------------------------------------
# ELIMINAR DUPLICADOS
# --------------------------------------------------
def delete_duplicates(folder):
    hashes = {}
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            filehash = file_hash(file_path)
            if filehash in hashes:
                os.remove(file_path)
            else:
                hashes[filehash] = file_path


# --------------------------------------------------
# ELIMINAR UN ARCHIVO
# --------------------------------------------------
def delete_file(folder):
    file_path = filedialog.askopenfilename(initialdir=folder, title="Selecciona el archivo a eliminar")
    if not file_path or not os.path.exists(file_path):
        messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo o no existe")
        return False

    confirm = messagebox.askyesno("Confirmar eliminación", f"¿Seguro que quieres eliminar este archivo?\n\n{file_path}")
    if confirm:
        try:
            os.remove(file_path)
            messagebox.showinfo("Éxito", "Archivo eliminado correctamente")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
            return False

    return False