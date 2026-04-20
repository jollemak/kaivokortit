from services.ai import MistralOCR
from config import MISTRAL_KEY
from main import OCRMetadataResponse

class OCRProcessingError(RuntimeError):
    """Raised when OCR processing fails for a recoverable reason."""

def analyze_pdf_bytes(pdf_bytes: bytes) -> OCRMetadataResponse:
    if not pdf_bytes:
        raise OCRProcessingError("Uploaded PDF is empty")
    try:
        ocr = MistralOCR(api_key=MISTRAL_KEY)
        response = ocr.analyze_pdf(pdf_bytes)
    except Exception as e:
        print(f'Error with ocr process: {e}')
    
    return response

