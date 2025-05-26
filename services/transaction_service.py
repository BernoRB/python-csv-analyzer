import csv
import os
import time
from typing import List, Dict
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from collections import defaultdict

ANALYSIS_SUSPICIOUS = "sospechosas"
ANALYSIS_GROUPED = "agrupadas"
VALID_ANALYSIS_TPYES = [ANALYSIS_SUSPICIOUS, ANALYSIS_GROUPED]

class TransactionService:

  async def process_file(self, file: UploadFile, analysis_type: str) -> FileResponse:
    """Procesa archivo y retorna CSV con los resultados"""

    # Read uploaded file
    transactions = await self._read_csv(file)

    # Make requested analysis
    if analysis_type == ANALYSIS_SUSPICIOUS:
      pass
    elif analysis_type == ANALYSIS_GROUPED:
      pass

    else:
      raise HTTPException(status_code=400, detail="Tipo de análisis no válido")
    
    return self._create_csv_response()


  async def _read_csv(self, file: UploadFile) -> List[Dict]:
    """Lee CSV desde archivo subido"""
    try:
      pass

    except Exception as e:
      raise HTTPException(status_code=400, detail=f"Error leyendo CSV: {str(e)}")

  
  def _create_csv_response(self, data: List[Dict], filename: str, headers: List[str]) -> StreamingResponse:
    """Crea respuesta CSV"""
    pass


  def _analyze_suspicious(self, transactions: List[Dict]) -> List[Dict]:
    """Detecta y devuelve transacciones sospechosas"""
    pass


  def _analyze_grouped(self, transactions: List[Dict]) -> List[Dict]:
    """Agrupa y devuelve transacciones por usuario"""
    pass