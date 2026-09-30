# LegalEase — System Architecture Document

## 1. Architecture Overview

LegalEase follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT FRONTEND                        │
│  (app.py - User Interface, Input Collection, Preview)       │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP POST /generate
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                           │
│  (backend/main.py, backend/routes.py, backend/schemas.py)   │
│  - Request Validation (Pydantic)                            │
│  - Route Handling                                           │
│  - Response Formatting                                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI SERVICE LAYER                          │
│  (ai_core/gemini_generator.py)                              │
│  - Prompt Construction                                      │
│  - Gemini API Integration                                   │
│  - Output Validation/Sanitization                           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 DOCUMENT GENERATION LAYER                    │
│  (document_generator/txt_generator.py)                      │
│  (document_generator/docx_generator.py)                     │
│  (document_generator/pdf_generator.py)                      │
│  - TXT Export                                               │
│  - DOCX Export (with logo, tables, formatting)               │
│  - PDF Export (with headers/footers, formatting)            │
└─────────────────────────────────────────────────────────────┘
```

## 2. Component Responsibilities

| Component | File(s) | Responsibility |
|-----------|---------|----------------|
| **Frontend** | `app.py` | Streamlit UI for input collection, document preview, editing, and download buttons |
| **API Entry** | `backend/main.py` | FastAPI application initialization, CORS middleware, health check endpoint |
| **API Routes** | `backend/routes.py` | POST /generate endpoint, request routing, response formatting |
| **Validation** | `backend/schemas.py` | Pydantic models for request/response validation |
| **AI Service** | `ai_core/gemini_generator.py` | Gemini API integration, prompt building, output sanitization |
| **TXT Generator** | `document_generator/txt_generator.py` | Plain text document export |
| **DOCX Generator** | `document_generator/docx_generator.py` | Word document generation with python-docx (logo, headings, tables, footer) |
| **PDF Generator** | `document_generator/pdf_generator.py` | PDF generation with reportlab (headers, footers, headings, paragraphs) |
| **Utilities** | `utils/helpers.py` | Date validation, text sanitization, file path handling |
| **Configuration** | `.env`, `.env.example` | Environment variables (API keys, model configuration) |

## 3. Data Flow

```
User Input (Streamlit)
    │
    ▼
┌─────────────────┐
│  Validation     │ ← Pydantic schemas validate all fields
│  (FastAPI)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Prompt         │ ← Build structured prompt with document type,
│  Construction   │   parties, terms, effective date
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gemini API     │ ← Send prompt to Google Gemini
│  Call           │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Output         │ ← Sanitize and validate AI response
│  Processing     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Response       │ ← Return JSON with document text + disclaimer
│  (FastAPI)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Preview & Edit │ ← Streamlit displays editable preview
│  (Streamlit)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Export         │ ← User selects TXT/DOCX/PDF
│  (Generators)   │
└─────────────────┘
```

## 4. Request/Response Flow

### Request (POST /generate)
```json
{
  "document_type": "NDA",
  "parties": "Party A: Acme Corp, Party B: Beta LLC",
  "terms_conditions": "Confidentiality period: 2 years. Governing law: Delaware.",
  "effective_date": "2026-09-30"
}
```

### Response (Success - 200 OK)
```json
{
  "success": true,
  "document": "NON-DISCLOSURE AGREEMENT\n\n...",
  "disclaimer": "This document is AI-generated for informational purposes...",
  "document_type": "NDA",
  "generated_at": "2026-09-30T10:30:00Z"
}
```

### Response (Error - 400 Bad Request)
```json
{
  "success": false,
  "error": "Validation failed",
  "details": ["document_type is required", "effective_date must be a valid date"]
}
```

### Response (Error - 500 Internal Server Error)
```json
{
  "success": false,
  "error": "AI generation failed",
  "details": "Unable to generate document. Please try again."
}
```

## 5. Error Flow

```
User Input Error
    │
    ▼
┌─────────────────┐
│  Pydantic       │ ← Returns 400 with field-specific errors
│  Validation     │
└─────────────────┘

AI Service Error
    │
    ▼
┌─────────────────┐
│  Retry Logic    │ ← Retry once on transient failures
│  (1 attempt)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Error Response │ ← Returns 500 with user-friendly message
│  (No API key    │   (never expose internal details)
│   exposure)    │
└─────────────────┘

Document Generation Error
    │
    ▼
┌─────────────────┐
│  Fallback       │ ← Log error, return meaningful message
│  Handling       │
└─────────────────┘
```

## 6. Security Flow

```
API Key Input
    │
    ▼
┌─────────────────┐
│  .env File      │ ← Key stored in environment variable
│  (GEMINI_API_KEY)│   (never in code, never in Git)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Environment    │ ← Loaded via python-dotenv at runtime
│  Variable Load  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  API Call       │ ← Key sent only to Google Gemini API
│  (HTTPS only)  │   (never logged, never returned in responses)
└─────────────────┘

Input Validation
    │
    ▼
┌─────────────────┐
│  Pydantic       │ ← All inputs validated for type, length,
│  Validation     │   and content (prevent injection)
└─────────────────┘

Error Handling
    │
    ▼
┌─────────────────┐
│  Sanitized      │ ← Error messages never expose API keys,
│  Errors         │   internal paths, or stack traces
└─────────────────┘
```

## 7. API Flow

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check - confirms backend is running |
| POST | `/generate` | Generate legal document from user inputs |

### POST /generate Flow

```
1. Receive JSON request
2. Validate with Pydantic (DocumentRequest schema)
3. If invalid → Return 400 with error details
4. If valid → Build prompt with document type, parties, terms, date
5. Call Gemini API with prompt
6. If API fails → Retry once → If still fails, return 500
7. Sanitize AI output
8. Append legal disclaimer
9. Return JSON response with document text
```

## 8. Deployment Architecture

### Local Development
```
┌─────────────────┐     ┌─────────────────┐
│  Streamlit      │     │  FastAPI        │
│  (localhost:8501)│────▶│  (localhost:8000)│
└─────────────────┘     └─────────────────┘
```

### Production Deployment Options

#### Option A: Render/Railway (Platform-as-a-Service)
```
┌─────────────────┐     ┌─────────────────┐
│  Streamlit      │     │  FastAPI        │
│  (Render Web    │────▶│  (Render Web    │
│   Service)      │     │   Service)      │
└─────────────────┘     └─────────────────┘
```

#### Option B: Docker Containerization
```
┌─────────────────────────────────────────┐
│              Docker Container           │
│  ┌─────────────┐    ┌─────────────┐    │
│  │  Streamlit  │───▶│  FastAPI    │    │
│  │  (Port 8501)│    │  (Port 8000)│    │
│  └─────────────┘    └─────────────┘    │
└─────────────────────────────────────────┘
```

#### Option C: VPS (DigitalOcean/AWS EC2)
```
┌─────────────────┐     ┌─────────────────┐
│  Nginx          │     │  Docker Compose │
│  (Reverse Proxy)│────▶│  (Streamlit +   │
│                 │     │   FastAPI)      │
└─────────────────┘     └─────────────────┘
```

## 9. Project Structure

```
LegalEase/
│
├── app.py                          # Streamlit frontend entry point
│
├── backend/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app initialization
│   ├── routes.py                   # API route definitions
│   └── schemas.py                  # Pydantic validation models
│
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py         # Gemini AI integration
│
├── document_generator/
│   ├── __init__.py
│   ├── txt_generator.py            # TXT export
│   ├── docx_generator.py           # DOCX export
│   └── pdf_generator.py            # PDF export
│
├── utils/
│   ├── __init__.py
│   └── helpers.py                  # Utility functions
│
├── assets/
│   └── logo/
│       └── logo.png                # Default logo (optional)
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py                 # API endpoint tests
│   ├── test_ai.py                  # AI service tests
│   ├── test_document_generation.py # Document export tests
│   └── test_integration.py         # End-to-end tests
│
├── .env                            # Environment variables (NEVER commit)
├── .env.example                    # Template for environment variables
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── LICENSE                         # License file
└── LegalEase_FRD.md                # Functional Requirements Document
```

## 10. Technology Justification

| Technology | Purpose | Justification |
|------------|---------|---------------|
| **Streamlit** | Frontend | Rapid UI development, built-in widgets, Python-native |
| **FastAPI** | Backend | Async support, automatic OpenAPI docs, Pydantic integration |
| **Google Gemini** | AI Model | State-of-the-art language model, Google AI SDK available |
| **python-docx** | DOCX Generation | Native Word document support, table/heading formatting |
| **reportlab** | PDF Generation | Professional PDF layout, header/footer support |
| **Pydantic** | Validation | Type safety, automatic validation, FastAPI integration |
| **python-dotenv** | Config | Secure environment variable management |

---
*This architecture will guide Phase 3 (Git Initialization) and all subsequent development phases.*