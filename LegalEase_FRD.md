# LegalEase — Functional Requirements Document (FRD)

## 1. Introduction

### 1.1 Project Name
LegalEase – AI-Powered Legal Document Generator

### 1.2 Purpose
Provide a web-based application that generates professional legal documents (contracts, NDAs, lease agreements, employment documents) using Google Gemini AI, with a Streamlit frontend and FastAPI backend, supporting multiple export formats (TXT, DOCX, PDF) and editable preview.

### 1.3 Scope
- **In Scope**:
  - Document generation for 4+ legal document types
  - User input collection (parties, terms, effective date)
  - AI-powered document generation via Google Gemini
  - Editable preview within Streamlit UI
  - TXT, DOCX, and PDF export with professional formatting
  - Logo/branding support
  - Secure API key handling via environment variables
  - Local testing and deployment preparation

- **Out of Scope**:
  - Multi-user deployment with authentication (beyond local use)
  - Legally binding document certification
  - Real-time collaborative editing
  - Cloud storage integration (beyond temporary generation)

### 1.4 Objectives
- Streamline legal document creation for individuals and small businesses
- Provide professional formatting without requiring legal expertise
- Ensure AI-generated content includes appropriate disclaimers
- Enable export in common document formats
- Maintain secure handling of API keys and user data

## 2. Stakeholders

| Stakeholder | Role |
|-------------|------|
| **End User** | Generates and exports legal documents using the application |
| **System Administrator/Developer** | Maintains the system, configures API keys, handles deployments |
| **AI Service Provider** | Google Gemini (provides the AI model for document generation) |

## 3. Functional Requirements

| Requirement ID | Description | Priority | Input | Processing | Output | Acceptance Criteria |
|----------------|-------------|----------|-------|------------|--------|---------------------|
| **FR-001** | User shall be able to select a legal document type | High | Document type selector (Contract, NDA, Lease Agreement, Employment Document) | UI captures selected type | Selected type is passed to backend | User can choose from documented document types |
| **FR-002** | User shall be able to enter involved parties | High | Parties text input (e.g., "Landlord: John Doe, Tenant: Jane Smith") | UI captures parties string | Parties string is passed to AI prompt | Parties field is validated and non-empty |
| **FR-003** | User shall be able to enter terms and conditions | High | Terms/conditions text area | UI captures long text string | Text is included in AI prompt | User can enter multiple clauses; field supports rich text |
| **FR-004** | User shall be able to provide an effective date | Medium | Date picker input | UI captures date | Date is included in document and prompt | Date is valid and formatted consistently |
| **FR-005** | System shall generate the legal document using the configured AI model | High | All user inputs (type, parties, terms, date) + API key | Backend sends structured prompt to Gemini API | AI-generated document text | Document is generated; AI disclaimer is included |
| **FR-006** | User shall be able to preview the generated document | Medium | Generated document text from backend | Streamlit displays markdown/editable area | User sees formatted preview | Preview matches generated content; user can read all sections |
| **FR-007** | User shall be able to edit generated content | Medium | Preview text + user edits | UI captures edited text | Edited text is re-saved/used for export | User can modify any part of the document; changes persist for export |
| **FR-008** | User shall be able to download the document as TXT | High | Final document text (edited or raw) | Convert to plain text format | .txt file downloaded | File downloads successfully; contains full document text |
| **FR-009** | User shall be able to download the document as DOCX | High | Final document text + formatting instructions | Generate Word document with title, headings, paragraphs, table, footer | .docx file downloaded | File opens in Word; professional formatting applied; logo included if configured |
| **FR-010** | User shall be able to download the document as PDF | High | Final document text + formatting instructions | Generate PDF with header/footer, headings, paragraphs, terms formatting | .pdf file downloaded | File opens in PDF reader; header/footer present; clean layout |
| **FR-011** | System shall support multiple document types (contracts, NDAs, lease agreements, employment documents) | High | Document type selection | Backend routes to appropriate prompt template | Document generated with type-specific sections | Each document type generates appropriate clauses/structure |
| **FR-012** | System shall include professional formatting (headings, paragraphs, tables) | High | Document content from AI | Backend/formatting module structures output | Formatted DOCX/PDF output | Output has consistent headings, paragraph styles, and tables where appropriate |
| **FR-013** | System shall support logo/branding integration | Medium | Optional logo file upload | Logo image is embedded in DOCX/PDF headers | Branded document output | Logo appears at top of DOCX/PDF; default placeholder if none provided |
| **FR-014** | System shall include terms/clauses table where applicable | Medium | AI-generated clauses | Formatting module creates table | Table in DOCX/PDF showing clauses | Table is present in output for document types that benefit from tabular format |
| **FR-015** | System shall support headers/footers where applicable | Medium | Document metadata (title, page info) | Formatting module adds headers/footers to PDF/DOCX | Header/footer in exported files | PDF has page headers/footers; DOCX has header text if applicable |
| **FR-016** | User shall be able to securely input and store API key | High | Gemini API key text input | Key is loaded from .env file; never exposed in UI or logs | API key is available to backend | Key works for Gemini API calls; .env is in .gitignore |
| **FR-017** | System shall generate AI content with appropriate disclaimer | High | AI-generated document text | Disclaimer text is prepended/appended | Document with legal disclaimer | Disclaimer states content is informational and should be reviewed by legal professional |
| **FR-018** | System shall allow local testing and deployment | High | Full system run locally | All components function on localhost | System runs and is testable | Backend API responds; Streamlit page loads; generation works end-to-end |

## 4. Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| **Performance** | Document generation should complete within 30–60 seconds per document (depending on AI response time). |
| **Security** | API keys must never be hard-coded or exposed in client-side code or logs. Use `.env` file and environment variables. `.gitignore` must exclude `.env`, `*.pyc`, `__pycache`, `.venv/`, `venv/`, `.DS_Store`. |
| **Reliability** | System should handle missing/invalid inputs gracefully without crashing; display user-friendly error messages. |
| **Maintainability** | Code should be modular with separated concerns (API routes, AI service, document formatting). |
| **Usability** | Streamlit UI should be intuitive, with clear labels, instructions, and error messages. |
| **Scalability** | Designed for single-user local use; can be scaled to multi-user via deployment on Render/Railway/Streamlit Community Cloud. |
| **Availability** | Local deployment; accessible whenever the server is running. |
| **Data Privacy** | User inputs (parties, terms) are processed via Gemini API; no persistent storage required beyond transient generation. |

## 5. Use Cases

### UC-001: Generate Legal Document

| Field | Details |
|-------|---------|
| **Actor** | End user |
| **Preconditions** | User has valid Gemini API key in `.env`; user is on the generator page |
| **Main Flow** | 1. User selects document type from dropdown<br>2. User enters involved parties in text field<br>3. User enters terms and conditions in text area<br>4. User selects effective date from date picker<br>5. User clicks "Generate Document" button<br>6. Streamlit sends request to FastAPI<br>7. FastAPI validates inputs<br>8. FastAPI calls Gemini AI with structured prompt<br>9. AI returns generated document text<br>10. FastAPI adds disclaimer and returns response<br>11. Streamlit displays preview with generated document<br>12. User can edit preview or proceed to download |
| **Alternative Flow** | If API key is invalid or missing, user receives error message prompting to check `.env` |
| **Exception Flow** | If Gemini API fails, system retries once then shows error; if inputs are missing, validation prevents generation |
| **Postconditions** | Generated document is displayed in preview; user can download in TXT/DOCX/PDF format |

### UC-002: Preview Document

| Field | Details |
|-------|---------|
| **Actor** | End user |
| **Preconditions** | Document has been generated (UC-001 completed) |
| **Main Flow** | 1. Generated text is displayed in Streamlit editable area<br>2. User can read all sections<br>3. User can scroll through document |
| **Alternative Flow** | If no document generated, user is prompted to generate first |
| **Postconditions** | User can review document before editing/exporting |

### UC-003: Edit Document

| Field | Details |
|-------|---------|
| **Actor** | End user |
| **Preconditions** | Document preview is visible (UC-002) |
| **Main Flow** | 1. User modifies text in preview area<br>2. User clicks outside or saves edits<br>3. Edited text is captured and used for subsequent exports |
| **Alternative Flow** | User cancels editing and returns to input form |
| **Postconditions** | Edited content is saved and available for download exports |

### UC-004: Download TXT

| Field | Details |
|-------|---------|
| **Actor** | End user |
| **Preconditions** | Document preview is visible (may be edited) |
| **Main Flow** | 1. User clicks "Download as TXT" button<br>2. System converts final text to plain TXT format<br>3. Browser initiates download of `.txt` file<br>4. File contains full document text without formatting |
| **Postconditions** | User has TXT copy of document |

### UC-005: Download DOCX

| Field | Details |
|-------|---------|
| **Actor** | End user |
| **Preconditions** | Document preview is visible (may be edited) |
| **Main Flow** | 1. User clicks "Download as DOCX" button<br>2. Formatting module generates Word document with title, headings, paragraphs, terms table, footer, and logo if available<br>3. Browser initiates download of `.docx` file |
| **Postconditions** | User has professionally formatted Word document |

### UC-006: Download PDF

| Field | Details |
|-------|---------|
| **Actor** | End user |
| **Preconditions** | Document preview is visible (may be edited) |
| **Main Flow** | 1. User clicks "Download as PDF" button<br>2. Formatting module generates PDF with header/footer, headings, clean paragraphs, terms formatting<br>3. Browser initiates download of `.pdf` file |
| **Postconditions** | User has professional PDF document |

## 6. Traceability Matrix

| Requirement ID | Use Case | Module | Test Case |
|----------------|----------|--------|-----------|
| FR-001 | UC-001, UC-002, UC-003 | UI/Backend | TC-001: User selects document type from dropdown |
| FR-002 | UC-001, UC-002, UC-003 | UI/Backend | TC-002: User enters valid parties string |
| FR-003 | UC-001, UC-002, UC-003 | UI/Backend | TC-003: User enters terms and conditions |
| FR-004 | UC-001, UC-002, UC-003 | UI/Backend | TC-004: User selects effective date |
| FR-005 | UC-001 | AI Service | TC-005: AI generates document from prompt |
| FR-006 | UC-002 | Streamlit Frontend | TC-006: Preview displays generated text |
| FR-007 | UC-003 | Streamlit Frontend | TC-007: User edits preview content |
| FR-008 | UC-004 | Document Generator | TC-008: TXT export downloads correctly |
| FR-009 | UC-005 | Document Generator | TC-009: DOCX export with formatting downloads |
| FR-010 | UC-006 | Document Generator | TC-010: PDF export with headers/footers downloads |
| FR-011 | UC-001 | AI Service | TC-011: Different document types generate appropriate clauses |
| FR-012 | UC-005, UC-006 | Document Generator | TC-012: Professional formatting in DOCX/PDF |
| FR-013 | UC-005, UC-006 | Document Generator | TC-013: Logo appears in exported DOCX/PDF |
| FR-014 | UC-005, UC-006 | Document Generator | TC-014: Terms table present where applicable |
| FR-015 | UC-005, UC-006 | Document Generator | TC-015: Headers/footers present in exports |
| FR-016 | All | Configuration | TC-016: API key loaded from .env, not exposed |
| FR-017 | UC-001 | AI Service | TC-017: Disclaimer included in generated document |
| FR-018 | All | Deployment | TC-018: System runs locally end-to-end |

---
*This FRD will guide all subsequent phases. Each requirement will be implemented, tested, and verified against this document.*