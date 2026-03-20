import os
import shutil
import hashlib
from tkinter import filedialog, messagebox
from history import log_action


# --------------------------------------------------
# HASH DE ARCHIVO
# --------------------------------------------------

def file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

# --------------------------------------------------
# ORGANIZAR ARCHIVOS
# --------------------------------------------------

def organize_files(folder):
    selected_files = filedialog.askopenfilenames(
        initialdir=folder,
        title="Selecciona archivos"
    )

    if not selected_files:
        return False

    destination = filedialog.askdirectory(title="Selecciona carpeta destino")

    if not destination:
        return False

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

            log_action(f"Archivo movido: {file_path} -> {destination}")

            moved += 1

        except Exception as e:

            messagebox.showerror("Error", f"No se pudo mover {filename}\n{str(e)}")

    return moved > 0

# --------------------------------------------------
# ELIMINAR DUPLICADOS
# --------------------------------------------------

def delete_duplicates(folder):

    hashes = {}

    removed = 0

    for filename in os.listdir(folder):

        path = os.path.join(folder, filename)

        if not os.path.isfile(path):
            continue

        filehash = file_hash(path)

        if filehash in hashes:

            try:

                os.remove(path)

                log_action(f"Duplicado eliminado: {filename}")

                removed += 1

            except Exception as e:

                print(f"No se pudo eliminar {filename}: {e}")

        else:

            hashes[filehash] = path

    return removed


# --------------------------------------------------
# ELIMINAR ARCHIVOS (MULTIPLE)
# --------------------------------------------------

def delete_file(folder):

    files = filedialog.askopenfilenames(
        initialdir=folder,
        title="Selecciona archivos a eliminar"
    )

    if not files:

        messagebox.showwarning("Advertencia", "No se seleccionaron archivos")

        return False

    confirm = messagebox.askyesno(
        "Confirmar eliminación",
        f"¿Seguro que quieres eliminar {len(files)} archivos?"
    )

    if not confirm:
        return False

    removed = 0

    for file_path in files:

        try:

            os.remove(file_path)

            log_action(f"Archivo eliminado: {file_path}")

            removed += 1

        except Exception as e:

            messagebox.showerror("Error", str(e))

    messagebox.showinfo("Éxito", f"{removed} archivos eliminados")

    return True