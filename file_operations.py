import os, re, shutil, hashlib
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
    same_folder_error = False # Cuando seleccionas la misma carpeta

    for file_path in selected_files:
        try:
            filename = os.path.basename(file_path)
            destination_path = os.path.join(destination, filename)

            # Comprobacion del mismo directorio
            if os.path.abspath(os.path.dirname(file_path)) == os.path.abspath(destination):
                same_folder_error = True
                continue 
            
            # Generar nombre unico si ya existe
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

    # Si los archivos seleccionados ya estaban en la misma carpeta
    if same_folder_error and moved == 0:
        messagebox.showwarning("Error", "Los archivos seleccionados ya estan en esa misma carpeta")
        return False
    
    # Devuelve True solo si movió al menos un archivo
    return moved > 0

# --------------------------------------------------
# ELIMINAR DUPLICADOS
# --------------------------------------------------
def delete_duplicates(folder):
    removed = 0
    items = os.listdir(folder)

    originals = {}

    for item in items:
        path = os.path.join(folder, item)
        name, ext = os.path.splitext(item)
        base_name = re.sub(r'(\(\d+\)|\d+)$', '', name)

        if not re.search(r'(\(\d+\)|\d+)$', name):
            originals[base_name] = item
        
    # Eliminamos duplicados
    for items in items:
        path = os.path.join(folder, item)
        name, ext = os.path.splitext(item)
        base_name = re.sub(r'(\(\d+\)|\d+)$', name)

        # Si existe original y este item NO es el original -> eliminar
        if base_name in originals and item != originals[base_name]:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                removed += 1
            except Exception as e:
                print(f"No se pudo eliminar {item}: {e}")

    return removed

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