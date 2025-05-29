from fastapi import FastAPI, File, Form, UploadFile, HTTPException

from services.transaction_service import TransactionService

app = FastAPI(
  title="CSV Transactions Analyzer",
  version="1.2.1"
)


@app.post("/files")
async def analyze_transactions(
  file: UploadFile = File(...),
  analysis_type: str = Form(...)
):
  """Analiza CSV de transacciones"""
  # Validate file type
  if not file.filename.endswith('.csv'):
    raise HTTPException(status_code = 400, detail = "Solo se permiten archivos CSV")
  
  # Analysis
  service = TransactionService()
  return await service.process_file(file, analysis_type)


@app.get("/health")
def healt_check():
  """Healthcheck endpoint"""
  return {
    "status": "healthy!"
  }