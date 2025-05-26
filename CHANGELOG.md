# Changelog

## [1.2.0] - 2025-05-26
### Cambios
- Se cambia el enfoque: el archivo no será almacenado, ni el que ingresa ni el que sale, para simplificar el flujo.
- Ingresara el archivo, se hará el análisis requerido y se devolverá un CSV directamente.
### Añadido
- En base a los cambios definidos, se dividen mínimamente las responsabilidades añadiendo un servicio con el esqueleto de las funciones que tendrá (procesar, leer, crear respuesta, análisis de transacciones sospechosas y análisis de agrupación de transacciones)

## [1.1.0] - 2025-05-26
### Añadido
- Endpoint POST /files para subir archivos CSV
- Endpoint GET /files para listar archivos subidos
- Validacion de tipo (CSV), guardado con timestamp para evitar sobreescritura

## [1.0.0] - 2025-05-26
### Añadido
- Configuración inicial del proyecto con FastAPI
- Estructura básica de directorios
- Configuración de entorno virtual y dependencias