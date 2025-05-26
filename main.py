import time
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
import os
import shutil

app = FastAPI(
  title="CSV Transactions Analyzer",
  version="1.1.0"
)

# Uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/files")
async def upload_csv(file: UploadFile = File(...)):
  """Subir archivos csv"""

  # Validate file type
  if not file.filename.endswith('.csv'):
    raise HTTPException(
      status_code = 400,
      detail = "Solo se permiten archivos CSV"
    )
  
  # Add timestamp to filename to avoid overrides
  timestamp = int(time.time())
  filename_without_ext = os.path.splitext(file.filename)[0]
  extension = os.path.splitext(file.filename)[1]
  filename = f"{filename_without_ext}_{timestamp}{extension}"
  file_path = os.path.join(UPLOAD_DIR, filename)

  # Save file
  try:
    with open(file_path, "wb") as f:
      shutil.copyfileobj(file.file, f)
    return {
      "message": "Archivo subido exitosamente",
      "filename": file.filename,
      "size": os.path.getsize(file_path)
    }
  except Exception as e:
    raise HTTPException(
      status_code = 500,
      detail=f"Error al guardar el archivo: {str(e)}"
    )
  

@app.get("/files")
def list_files():
  """Listar archivos csv subidos"""
  files = []
  for f in os.listdir(UPLOAD_DIR):
    if f.endswith('.csv'):
      files.append(f)
  return {"files": files}

@app.get("/health")
def healt_check():
  """Healthcheck endpoint"""
  return {
    "status": "healthy!"
  }