import re

from schemas import OCRMetadataResponse

from mistralai.client import Mistral

KNOWN_COMPANIES = ["FCG", "Sitowise", "A-INSINÖÖRIT", "A-INSINÖRIT", "Destia", "AFRY"]

COMPANY_PATTERN = re.compile(
    r"|".join(re.escape(c) for c in KNOWN_COMPANIES),
    re.IGNORECASE,
)

CARD_PATTERN = re.compile(
    r"(?:KAIVO\s+N:O|KAIVO\s+NRO|KAIVO\s+N\.O|KAIVO\s+NO|Kaivon?\s+nro|Kaivotunnus)"
    r"\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-_/]{0,30})",
    re.IGNORECASE,
)

class MistralOCR():
    def __init__(self, api_key:str):
        self.api_key = api_key
        self.model = 'mistral-ocr-latest'
        self.client = Mistral(api_key=api_key)
    
    def analyze_pdf(self, pdf_url):
        ocr_response = self.client.ocr.process(
            model="mistral-ocr-latest",
            document={"type": "document_url", "document_url": pdf_url},
            confidence_scores_granularity="page",
        )
        page_markdowns: list[str] = []
        cards_by_page: dict[int, list[str]] = {}
        warnings: list[str] = []

        for page in ocr_response.pages:
            markdown = page.markdown or ""
            page_markdowns.append(markdown)

            cleaned = _clean_text(markdown)
            cards = _extract_cards_from_text(cleaned)
            if cards:
                cards_by_page[page.index + 1] = cards
            else:
                warnings.append(f"No card number matched on page {page.index + 1}")

        company_name = _extract_company_name(page_markdowns)
        if not company_name:
            warnings.append("Company name was not confidently extracted")

        return OCRMetadataResponse(
            company_name=company_name,
            cards_by_page=cards_by_page,
            warnings=warnings)
    
    
def _clean_text(markdown: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^\)]*\)", " ", markdown)
    text = re.sub(r"\[[^\]]*\]\([^\)]*\)", " ", text)
    text = re.sub(r"[`*_#>|]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_cards_from_text(text: str) -> list[str]:
    found: list[str] = []
    seen = set()

    for match in CARD_PATTERN.finditer(text):
        card = match.group(1).strip().upper()
        if card not in seen:
            seen.add(card)
            found.append(card)
    return found


def _extract_company_name(pages: list[str]) -> str | None:
    for page in pages:
        match = COMPANY_PATTERN.search(page)
        if match:
            matched_text = match.group(0).lower()
            for company in KNOWN_COMPANIES:
                if company.lower() == matched_text:
                    if company.lower() == "a-insinörit":
                        company = KNOWN_COMPANIES[2]
                    return company
    return None
    

   
    

    

    
    
        