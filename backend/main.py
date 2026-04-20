from fastapi import FastAPI, File, HTTPException, UploadFile
from schemas import OCRMetadataResponse

from api import OCRProcessingError, analyze_pdf_bytes

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "Hello World"}


@app.post("/ocr/analyze", response_model=OCRMetadataResponse)
async def analyze_well_cards(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        parsed = analyze_pdf_bytes(pdf_bytes=pdf_bytes, filename=file.filename or "document.pdf")
    except OCRProcessingError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {exc}") from exc

    return OCRMetadataResponse(
        company_name=parsed.company_name,
        cards_by_page=parsed.cards_by_page,
        warnings=parsed.warnings,
    )