from fastapi import FastAPI

app = FastAPI(
  title="CSV Transactions Analyzer",
  version="1.0.0"
)

@app.get("/")
def index():
  return {
    "message": "API working!"
  }

@app.get("/health")
def healt_check():
  return {
    "status": "healthy!"
  }