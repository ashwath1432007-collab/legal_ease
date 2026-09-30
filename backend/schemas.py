from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class DocumentRequest(BaseModel):
    document_type: str = Field(..., description="Type of legal document", min_length=1)
    parties: str = Field(..., description="Involved parties", min_length=1)
    terms_conditions: str = Field(..., description="Terms and conditions", min_length=1)
    effective_date: date = Field(..., description="Effective date of the document")

    class Config:
        json_schema_extra = {
            "example": {
                "document_type": "NDA",
                "parties": "Party A: Acme Corp, Party B: Beta LLC",
                "terms_conditions": "Confidentiality period: 2 years",
                "effective_date": "2026-09-30"
            }
        }


class DocumentResponse(BaseModel):
    success: bool
    document: Optional[str] = None
    disclaimer: Optional[str] = None
    document_type: Optional[str] = None
    generated_at: Optional[str] = None
    error: Optional[str] = None
    details: Optional[str] = None
