import streamlit as st
import requests
from datetime import date

st.set_page_config(
    page_title="LegalEase - AI Legal Document Generator",
    page_icon="⚖️",
    layout="wide"
)

API_URL = "http://localhost:8000"

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.markdown("""
**Disclaimer**: This tool generates AI-generated documents for informational purposes only.
All documents should be reviewed by a qualified legal professional before use.
""")

# Sidebar for inputs
with st.sidebar:
    st.header("Document Settings")

    document_type = st.selectbox(
        "Document Type",
        ["Contract", "NDA", "Lease Agreement", "Employment Document"]
    )

    parties = st.text_area(
        "Involved Parties",
        placeholder="e.g., Party A: Acme Corp, Party B: Beta LLC",
        help="Enter the names and details of all parties involved"
    )

    terms_conditions = st.text_area(
        "Terms & Conditions",
        placeholder="Enter specific terms, clauses, and conditions...",
        height=150,
        help="Describe the terms and conditions for the document"
    )

    effective_date = st.date_input(
        "Effective Date",
        value=date.today(),
        help="The date when the document becomes effective"
    )

    generate_button = st.button("Generate Document", type="primary", use_container_width=True)

# Main content area
if generate_button:
    if not parties.strip() or not terms_conditions.strip():
        st.error("Please fill in all required fields (Parties and Terms & Conditions).")
    else:
        with st.spinner("Generating your legal document..."):
            try:
                response = requests.post(
                    f"{API_URL}/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms_conditions": terms_conditions,
                        "effective_date": effective_date.isoformat()
                    },
                    timeout=120
                )

                if response.status_code == 200:
                    result = response.json()
                    st.session_state['document'] = result['document']
                    st.session_state['disclaimer'] = result['disclaimer']
                    st.success("Document generated successfully!")
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"Generation failed: {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Please ensure FastAPI is running on port 8000.")
            except requests.exceptions.Timeout:
                st.error("Request timed out. The AI service may be slow. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Document preview and editing
if 'document' in st.session_state:
    st.divider()
    st.subheader("Document Preview")

    edited_text = st.text_area(
        "Edit your document below:",
        value=st.session_state['document'],
        height=400
    )

    if st.session_state.get('disclaimer'):
        st.info(st.session_state['disclaimer'])

    # Download buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="Download TXT",
            data=edited_text.encode('utf-8'),
            file_name=f"{document_type.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        try:
            from document_generator.docx_generator import DOCXGenerator
            docx_bytes = DOCXGenerator.generate(edited_text, document_type)
            st.download_button(
                label="Download DOCX",
                data=docx_bytes,
                file_name=f"{document_type.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"DOCX export failed: {str(e)}")

    with col3:
        try:
            from document_generator.pdf_generator import PDFGenerator
            pdf_bytes = PDFGenerator.generate(edited_text, document_type)
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"{document_type.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF export failed: {str(e)}")
