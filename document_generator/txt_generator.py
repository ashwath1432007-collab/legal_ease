import io
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class TXTGenerator:
    @staticmethod
    def generate(document_text: str, document_type: str) -> bytes:
        """Generate TXT file content."""
        try:
            header = f"{document_type.upper()}\n"
            header += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            header += "=" * 60 + "\n\n"

            content = header + document_text
            return content.encode('utf-8')
        except Exception as e:
            logger.error(f"TXT generation error: {str(e)}")
            raise ValueError("Failed to generate TXT file")
