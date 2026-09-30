import io
import os
import logging
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

logger = logging.getLogger(__name__)


class PDFGenerator:
    @staticmethod
    def generate(document_text: str, document_type: str, logo_path: str = None) -> bytes:
        """Generate PDF file content."""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            styles = getSampleStyleSheet()
            story = []

            # Add logo if available
            if logo_path and os.path.exists(logo_path):
                img = Image(logo_path, width=1.5*inch, height=0.75*inch)
                img.hAlign = 'CENTER'
                story.append(img)
                story.append(Spacer(1, 12))

            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                alignment=TA_CENTER,
                spaceAfter=12
            )
            story.append(Paragraph(document_type.upper(), title_style))

            # Date
            date_style = ParagraphStyle(
                'DateStyle',
                parent=styles['Normal'],
                fontSize=10,
                alignment=TA_CENTER,
                spaceAfter=24
            )
            story.append(Paragraph(
                f"Generated: {datetime.now().strftime('%B %d, %Y')}",
                date_style
            ))

            # Content
            content_style = ParagraphStyle(
                'Content',
                parent=styles['Normal'],
                fontSize=11,
                alignment=TA_JUSTIFY,
                spaceAfter=6
            )

            lines = document_text.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    story.append(Spacer(1, 6))
                    continue
                if line.startswith('# '):
                    story.append(Spacer(1, 12))
                    story.append(Paragraph(line[2:], styles['Heading2']))
                elif line.startswith('## '):
                    story.append(Spacer(1, 8))
                    story.append(Paragraph(line[3:], styles['Heading3']))
                else:
                    story.append(Paragraph(line, content_style))

            # Build PDF with header/footer
            def add_header_footer(canvas, doc):
                canvas.saveState()
                # Header
                canvas.setFont('Helvetica', 8)
                canvas.drawString(72, letter[1] - 36, "LegalEase - AI-Powered Legal Document Generator")
                # Footer
                canvas.drawCentredString(letter[0]/2, 36, f"Page {doc.page}")
                canvas.restoreState()

            doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
            buffer.seek(0)
            return buffer.getvalue()

        except Exception as e:
            logger.error(f"PDF generation error: {str(e)}")
            raise ValueError("Failed to generate PDF file")
