from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.services.pdf_parser import extract_text_from_pdf

app = FastAPI()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
def root():
    return {"message": "Multi-model RAG backend is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = UPLOAD_DIR / file.filename

    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        extracted_text = extract_text_from_pdf(str(file_path))

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract any text from this PDF.")

        preview = extracted_text[:1000]

        return JSONResponse(
            content={
                "filename": file.filename,
                "message": "PDF uploaded and parsed successfully.",
                "characters_extracted": len(extracted_text),
                "preview": preview,
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")