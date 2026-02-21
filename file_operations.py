# FUNCIONES PARA CREAR, MOVER, COPIAR, RENOMBRAR Y ELIMINAR
import os
import shutil
import hashlib
from folder_operations import create_folder  # Importamos la función externa

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
    """
    Organiza archivos en subcarpetas según su extensión.
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            ext = filename.split('.')[-1]
            ext_folder = create_folder(folder, ext)  # usa la función importada
            shutil.move(file_path, os.path.join(ext_folder, filename))

def rename_files(folder):
    # lógica para renombrar
    pass

def delete_duplicates(folder):
    # lógica para eliminar duplicados
    pass