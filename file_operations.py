# FUNCIONES PARA CREAR, MOVER, COPIAR, RENOMBRAR Y ELIMINAR
import os, shutil, hashlib
from folder_operations import create_folder  # Importamos la función externa
from tkinter import filedialog, messagebox

# --- FUNCIONES AUXILIARES ---
def file_hash(file_path):
    """
    Devuelve un hash MD5 del archivo, útil para detectar duplicados.
    """
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


# --- FUNCIONES PRINCIPALES ---
def organize_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        if os.path.isfile(file_path):

            name, ext = os.path.splitext(filename)

            if not ext:
                ext = "sin_extension"
            else:
                ext = ext[1:]  # quitar el punto

            ext_folder = create_folder(folder, ext)
            shutil.move(file_path, os.path.join(ext_folder, filename))

def rename_files(folder):
    counter = 1

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        if os.path.isfile(file_path):
            name, ext = os.path.splitext(filename)
            new_name = f"archivo_{counter}{ext}"
            new_path = os.path.join(folder, new_name)

            os.rename(file_path, new_path)
            counter += 1

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

def delete_file(folder):
    # Seleccionar archivo dentro de la carpeta actual
    file_path = filedialog.askopenfilename(
        initialdir=folder,
        title="Selecciona el archivo a eliminar"
    )

    if not file_path:
        return False

    if not os.path.exists(file_path):
        messagebox.showwarning("Advertencia", "El archivo no existe")
        return False

    confirm = messagebox.askyesno(
        "Confirmar eliminación",
        f"¿Seguro que quieres eliminar este archivo?\n\n{file_path}"
    )

    if confirm:
        try:
            os.remove(file_path)
            messagebox.showinfo("Éxito", "Archivo eliminado correctamente")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{str(e)}")
            return False

    return False

# Organizar archivos
def organize_files(folder):
    # Seleccionar uno o varios archivos
    files = filedialog.askopenfilenames(
        initialdir=folder,
        title="Selecciona uno o varios archivos"
    )

    if not files:
        return

    # Seleccionar carpeta destino
    destination = filedialog.askdirectory(
        title="Selecciona la carpeta destino"
    )

    if not destination:
        return

    moved_count = 0

    for file_path in files:
        try:
            filename = os.path.basename(file_path)
            dest_path = os.path.join(destination, filename)

            # Evitar sobreescribir
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(
                    destination, f"{base}({counter}){ext}"
                )
                counter += 1

            shutil.move(file_path, dest_path)
            moved_count += 1

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mover:\n{str(e)}")
            return

    messagebox.showinfo(
        "Éxito",
        f"Se movieron {moved_count} archivo(s) correctamente"
    )