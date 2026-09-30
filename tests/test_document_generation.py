import pytest
from document_generator.txt_generator import TXTGenerator
from document_generator.docx_generator import DOCXGenerator
from document_generator.pdf_generator import PDFGenerator


def test_txt_generator():
    result = TXTGenerator.generate("Test document content", "NDA")
    assert isinstance(result, bytes)
    assert b"Test document content" in result
    assert b"NDA" in result


def test_docx_generator():
    result = DOCXGenerator.generate("Test document content", "Contract")
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_pdf_generator():
    result = PDFGenerator.generate("Test document content", "Lease Agreement")
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_txt_generator_empty():
    result = TXTGenerator.generate("", "NDA")
    assert isinstance(result, bytes)
