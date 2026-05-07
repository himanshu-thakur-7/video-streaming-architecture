from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def healthCheck():
    return {"status":"ok"}

@app.get("/ready")
def healthCheck():
    return {"status":"ready"}

