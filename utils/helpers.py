import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def sanitize_text(text: str) -> str:
    """Remove potentially harmful content from text."""
    if not text:
        return ""
    # Remove control characters except newlines and tabs
    sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return sanitized.strip()


def format_date(date_str: str) -> str:
    """Format date string for display."""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%B %d, %Y")
    except (ValueError, AttributeError):
        return date_str


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'


def validate_document_type(doc_type: str) -> bool:
    """Validate document type is supported."""
    valid_types = ["Contract", "NDA", "Lease Agreement", "Employment Document"]
    return doc_type in valid_types
