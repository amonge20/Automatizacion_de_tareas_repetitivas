# Automatizacion_de_tareas_repetitivas

# DESCRIPCION

Una herramienta de productividad diseñada para automatizar tareas repetitivas de gestión de archivos.

Con esta aplicación puedes organizar, renombrar, mover, copiar y eliminar archivos de manera rápida, sin depender del ratón ni de atajos de teclado. 
Todo se hace desde una interfaz sencilla de escritorio, pensada para ahorrar tiempo y mejorar tu flujo de trabajo.

Funcionalidades principales:

- Selección de carpetas de manera intuitiva

- Organización de archivos por tipo o extensión

- Renombrado masivo de archivos

- Eliminación de duplicados

- Copia o movimiento de archivos

- Barra de progreso y log de acciones realizadas

- Ideal para quienes manejan grandes cantidades de archivos y quieren simplificar tareas repetitivas con un solo clic.

# AVISO DE RESPONSABILIDAD

Esta aplicación se proporciona con fines educativos y empresariales.
El creador no se hace responsable de daños, pérdida de datos o cualquier manipulación indebida que pueda surgir del uso de esta herramienta.
Utilice la aplicación bajo su propia responsabilidad.
Cualquier uso comercial no autorizado será considerado una violación de los términos de uso y podrá ser reportado.

# CONTACTO

Si tienes preguntas, sugerencias o estás interesado en colaborar en este proyecto, no dudes en contactarme:  
**Correo:** [](mailto:)

# LENGUAJES DE PROGRAMACIÓN Y HERRAMIENTAS

- Python 3.13.12
- TKinter GUI

# ESTRUCTURA DEL PROYECTO 

file-manager/
├─ main.py                 # Código principal (Tkinter GUI)
├─ file_operations.py      # Funciones para borrar, renombrar, organizar archivos
├─ folder_operations.py    # Funciones para borrar, renombrar, organizar carpetas
├─ utils.py                # Funciones auxiliares (por ejemplo: verificar duplicados)
├─ requirements.txt        # Librerías necesarias (Tkinter incluido, opcionalmente others)
├─ README.md               # Explicación del proyecto, cómo usarlo
├─ LICENSE                 # Licencia del proyecto (ej: MIT)
├─ icons/                  # Iconos de la aplicación
├─ logs/                   # Archivos de registro de operaciones realizadas
└─ tests/                  # Pruebas unitarias opcionales
    └─ test_file_operations.py

# IDEA VISUAL

+-------------------------------------------------------------------+
|             GESTOR DE ARCHIVOS - V1.0                             |
+-------------------------------------------------------------------+
|                                                                   |
|  [Crear carpeta(cuando has seleccionado la carpeta)]              |
|  [Seleccionar carpeta]                                            |
|  [Ruta de la carpeta(despues de seleccionar la carpeta)]          |
|                                                                   |
|  Acciones disponibles:                                            |
|  --------------------                                             |
|  ( ) Organizar archivos   (BOTONES)                               |
|  ( ) Renombrar archivos   (BOTONES)                               |
|  ( ) Eliminar duplicados  (BOTONES)                               |
|  ( ) Copiar / Mover archivos  (BOTONES)                           |
|                                                                   |
|  Opciones adicionales:                                            |
|  [Barra de progreso]                                              |
|  [Mensajes de estado / confirmación]                              |
|                                                                   |
|  [Ejecutar acción]                                                |
|                                                                   |
|  Log de operaciones:                                              |
|  --------------------------------                                 |
|  - 2026-02-21: 5 archivos organizados                             |
|  - 2026-02-21: 2 duplicados eliminados                            |
|  ...                                                              |
+-------------------------------------------------------------------+
|                 Pie de página / Créditos                          |
+-------------------------------------------------------------------+
