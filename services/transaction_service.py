import csv
import io
from typing import List, Dict
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
import codecs
import os
from dotenv import load_dotenv

load_dotenv()

ANALYSIS_SUSPICIOUS = os.getenv('ANALYSIS_SUSPICIOUS', 'sospechosas')
ANALYSIS_GROUPED = os.getenv('ANALYSIS_GROUPED', 'agrupadas')
VALID_ANALYSIS_TPYES = [ANALYSIS_SUSPICIOUS, ANALYSIS_GROUPED]
BLACKLISTED_USERS = os.getenv('BLACKLISTED_USERS', '').split(',')
THRESHOLD_TX_AMMOUNT = float(os.getenv('THRESHOLD_TX_AMMOUNT', 130))

class TransactionService:

  async def process_file(self, file: UploadFile, analysis_type: str) -> StreamingResponse:
    """Procesa archivo y retorna CSV con los resultados"""

    # Read uploaded file
    transactions = await self._read_csv(file)
    # print(transactions)
    base_filename = file.filename.replace('.csv', '')

    # Make requested analysis
    if analysis_type == ANALYSIS_SUSPICIOUS:
      processed_data = self._analyze_suspicious(transactions)
      result_filename = f"{base_filename}_suspicious_transactions.csv"
      result_headers = ['usuario', 'fecha', 'monto', 'razon_sospecha']
    elif analysis_type == ANALYSIS_GROUPED:
      processed_data = self._analyze_grouped(transactions)
      result_filename = f"{base_filename}_grouped_transactions.csv"
      result_headers = ['usuario', 'cantidad', 'monto', 'monto_promedio']
    else:
      raise HTTPException(status_code=400, detail="Tipo de análisis no válido")
    
    return self._create_csv_response(processed_data, result_filename, result_headers)


  async def _read_csv(self, file: UploadFile) -> List[Dict]:
    """Lee CSV desde archivo subido"""
    try:
      csv_reader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))      
      transactions = []
      for row in csv_reader:
        transactions.append({
          'usuario': row['usuario'],
          'fecha': row['fecha'],
          'monto': float(row['monto'])
        })

      file.file.close()
      return transactions

    except Exception as e:
      raise HTTPException(status_code=400, detail=f"Error leyendo CSV: {str(e)}")

  
  def _create_csv_response(self, data: List[Dict], filename: str, headers: List[str]) -> StreamingResponse:
    """Crea respuesta CSV"""
    csv_lines = []

    # Add headers, putting a comma between each
    csv_lines.append(';'.join(headers)) # Nota personal Python: append agrega al final, normal. El ','.join(x) es 'unime todo lo de X usando , como separador'... en Node seria headers.join(',')

    # Add values to the csv lines from data dict
    for row in data:
      line_values = []
      for header in headers:
        if header in row:
          line_values.append(str(row[header]))
        else:
          line_values.append('')
      csv_lines.append(';'.join(line_values))
        
    # Add new line after each line
    csv_content = '\n'.join(csv_lines)

    # Convert to bytes to return
    csv_bytes = io.BytesIO(csv_content.encode('utf-8'))

    return StreamingResponse(
      csv_bytes,
      media_type='text/csv',
      headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


  def _analyze_suspicious(self, transactions: List[Dict]) -> List[Dict]:
    """Detecta y devuelve transacciones sospechosas"""
    
    result = []
    # Loop transactions and "mark" those suspicious
    for t in transactions:
      if(t['monto'] >= THRESHOLD_TX_AMMOUNT):
        result.append({
          'usuario': t['usuario'],
          'fecha': t['fecha'],
          'monto': t['monto'],
          'razon_sospecha': 'MONTO TRANSACCION'
      })
      elif(t['usuario'] in BLACKLISTED_USERS):
        result.append({
          'usuario': t['usuario'],
          'fecha': t['fecha'],
          'monto': t['monto'],
          'razon_sospecha': 'USER LISTA NEGRA'
      })

    return result


  def _analyze_grouped(self, transactions: List[Dict]) -> List[Dict]:
    """Agrupa y devuelve transacciones por usuario"""

    result = []
    # Loop txs, group them by user
    user_groups = {}
    for t in transactions:
      if(t['usuario'] not in user_groups):
        user_groups[t['usuario']] = []
      user_groups[t['usuario']].append(t)

    # Loop by user and aggregate all the txs
    for user in user_groups:
      agg_q = 0
      agg_amount = 0
      for t in user_groups[user]:
        agg_q += 1
        agg_amount += t['monto']
      result.append({
        'usuario': user,
        'cantidad': agg_q,
        'monto': agg_amount,
        'monto_promedio': round(agg_amount / agg_q, 2)
      })
    
    return result
    