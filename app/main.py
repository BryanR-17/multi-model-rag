from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Multi-model RAG backend is running"}