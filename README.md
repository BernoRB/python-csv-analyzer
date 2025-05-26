# python-csv-analyzer
Pequeño proyecto de automatización con Python para ingestar CSVs, procesarlos y obtener algún output en base a ellos.

## Instalación
1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno: `source venv/bin/activate` (Linux/Mac) o `venv\Scripts\activate` (Windows)
4. Instalar dependencias: `pip install -r requirements.txt`

## Ejecutar
```bash
uvicorn main:app --reload