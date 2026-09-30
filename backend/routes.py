import os
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from backend.schemas import DocumentRequest, DocumentResponse
from ai_core.gemini_generator import GeminiGenerator

logger = logging.getLogger(__name__)
router = APIRouter()
generator = GeminiGenerator()


@router.post("/generate", response_model=DocumentResponse)
async def generate_document(request: DocumentRequest):
    try:
        logger.info(f"Generating document of type: {request.document_type}")

        document_text = await generator.generate(
            document_type=request.document_type,
            parties=request.parties,
            terms_conditions=request.terms_conditions,
            effective_date=request.effective_date.isoformat()
        )

        disclaimer = (
            "DISCLAIMER: This document is AI-generated for informational purposes only. "
            "It should be reviewed by a qualified legal professional before use. "
            "The creators of LegalEase are not responsible for the legal validity of this document."
        )

        return DocumentResponse(
            success=True,
            document=document_text,
            disclaimer=disclaimer,
            document_type=request.document_type,
            generated_at=datetime.utcnow().isoformat()
        )

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Generation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate document. Please try again."
        )
