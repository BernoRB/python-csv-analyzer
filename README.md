# CSV Transactions Analyzer
Analizador de transacciones CSV que permite cargar un archivo, elegir un analisis (detectar actividad sospechosa o agrupa transacciones por usuario) y te devuelve un CSV con los resultados procesados. Proyecto sencillo que hice porque quería probar Python + FastAPI.
 
## Características/flujo
-Permite cargar un archivo CSV desde la interfaz web (se puede probar también desde una herramienta como Postman o desde la ruta OpenAPI /docs)
-Permite seleccionar el tipo de analisis desde la interfaz web, habiendo dos tipos de análisis a elegir: 
  1) Actividad sospechosa: devolverá en otro CSV las transacciones que superen X monto determinado por variable de entorno y también las transacciones por usuarios que estén en una 'lista negra de usuarios', configurable también por variable de entorno.
  2) Agrupación: devolverá otro CSV con las transacciones agrupadas por usuario, indicando la cantidad realizada, el monto $ total y el monto $ promedio. 
-Al cargarlo y elegir hará el análisis y devolverá otro CSV con los resultados.

## Instalación

1. Clonar repositorio:
```bash
git clone https://github.com/BernoRB/python-csv-analyzer.git
cd python-csv-analyzer
```

2. Instalar dependencias:
```bash
pip install fastapi uvicorn python-dotenv
```

3. Configurar variables de entorno (`.env`):
```env
ANALYSIS_SUSPICIOUS=sospechosas
ANALYSIS_GROUPED=agrupadas
BLACKLISTED_USERS=usuario1,usuario2
THRESHOLD_TX_AMMOUNT=130
```

4. Ejecutar servidor:
```bash
uvicorn main:app --reload
```

## Formato CSV esperado

```csv
usuario,fecha,monto
berno_rb,29/05/2025,10.0
juanjo_cr,29/05/2025,40.0
```
Puedes utilizar de ejemplo el archivo "txs_procesador_ejemplo.csv" que está en el root de este mismo proyecto.

## API Endpoints

- `POST /files` - Analizar archivo CSV
- `GET /health` - Estado del servidor