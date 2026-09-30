# LegalEase - AI-Powered Legal Document Generator

## Project Overview

LegalEase is an AI-powered legal document generator that enables users to create, preview, edit, and export professional legal documents (contracts, NDAs, lease agreements, employment documents) using Google Gemini AI.

## Features

- AI-powered legal document generation via Google Gemini
- Support for multiple document types (Contracts, NDAs, Lease Agreements, Employment Documents)
- Editable document preview
- Export to TXT, DOCX, and PDF formats
- Professional formatting with headers, footers, and tables
- Logo/branding support
- Secure API key handling via environment variables

## Architecture

```
Streamlit UI → FastAPI REST API → Validation Layer → AI Service (Gemini) → Document Generation → TXT/DOCX/PDF
```

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **AI**: Google Gemini
- **Document Generation**: python-docx, reportlab
- **Validation**: Pydantic

## Project Structure

```
LegalEase/
├── app.py                  # Streamlit frontend
├── backend/
│   ├── main.py             # FastAPI application
│   ├── routes.py           # API routes
│   └── schemas.py          # Pydantic models
├── ai_core/
│   └── gemini_generator.py # Gemini AI integration
├── document_generator/
│   ├── txt_generator.py    # TXT export
│   ├── docx_generator.py   # DOCX export
│   └── pdf_generator.py    # PDF export
├── utils/
│   └── helpers.py          # Utility functions
├── tests/                  # Test suite
├── .env                    # Environment variables (not committed)
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Prerequisites

- Python 3.11 or higher
- Google Gemini API key (get from https://makersuite.google.com/app/apikey)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd LegalEase
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   copy .env.example .env
   ```
   Edit `.env` and add your Gemini API key.

## Running the Application

### Start the Backend (FastAPI)
```bash
uvicorn backend.main:app --reload --port 8000
```

### Start the Frontend (Streamlit)
```bash
streamlit run app.py
```

## API Endpoints

- `GET /` - Health check
- `POST /generate` - Generate legal document

### Example Request
```json
{
  "document_type": "NDA",
  "parties": "Party A: Acme Corp, Party B: Beta LLC",
  "terms_conditions": "Confidentiality period: 2 years",
  "effective_date": "2026-09-30"
}
```

### Example Response
```json
{
  "success": true,
  "document": "NON-DISCLOSURE AGREEMENT...",
  "disclaimer": "This document is AI-generated...",
  "document_type": "NDA",
  "generated_at": "2026-09-30T10:30:00Z"
}
```

## Testing

Run all tests:
```bash
pytest tests/ -v
```

## Git Workflow

- `main` branch for production-ready code
- Feature branches for new development
- Commit messages follow conventional commits format

## Deployment

### Local Development
Run backend and frontend separately as shown above.

### Production Options
- **Render/Railway**: Deploy as web services
- **Docker**: Containerize both services
- **VPS**: Use Docker Compose with Nginx reverse proxy

## Security Notes

- API keys are stored in `.env` file and never committed
- `.gitignore` excludes sensitive files
- Input validation prevents injection attacks
- Error messages never expose internal details

## Legal Disclaimer

This application generates AI-generated content for informational purposes only. All generated documents should be reviewed by a qualified legal professional before use. The creators of this application are not responsible for the legal validity of generated documents.

## Future Improvements

- User authentication and document history
- Template customization
- Additional document types
- Cloud storage integration
- Multi-language support
