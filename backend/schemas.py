from pydantic import BaseModel

class OCRMetadataResponse(BaseModel):
    company_name: str | None
    cards_by_page: dict[int, list[str]]
    warnings: list[str] = []
