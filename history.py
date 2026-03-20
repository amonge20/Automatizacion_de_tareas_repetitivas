import datetime

# Crea un fichero para el historial
def log_action(action):

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("historial.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {action}\n")

# Lee los cambios que has hecho en el programa
def read_history():
    try:
        with open("historial.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "No hay historial todavía."
    
# Reiniciar el historial cada vez que inicias la aplicacion
def reset_history():
    with open("historial.txt", "w", encoding="utf-8") as f:
        f.write("")