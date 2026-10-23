import streamlit as st
import pymupdf
from ai_analyzer import analyze_with_ai
from matching import calculate_match

st.set_page_config(page_title="AI Job Application Assistant", page_icon="🤖", layout="wide")


def extract_pdf_text(uploaded_file):
    try:
        with pymupdf.open(stream=uploaded_file.getvalue(), filetype="pdf") as doc:
            if doc.page_count > 15:
                raise ValueError("Please upload a resume of 15 pages or fewer.")
            return "\n".join(page.get_text() for page in doc).strip()
    except Exception as exc:
        st.error(f"Could not read PDF: {exc}")
        return ""


st.title("🤖 AI Job Application Assistant")
st.caption("Educational skills-coverage analysis; not a hiring prediction.")
left, right = st.columns(2)
with left:
    uploaded = st.file_uploader("Upload a PDF resume", type=["pdf"])
with right:
    job_text = st.text_area("Paste a job description", height=220)

if st.button("Analyze Resume", type="primary"):
    if uploaded is None or not job_text.strip():
        st.warning("Upload a resume and enter a job description.")
    elif uploaded.size > 5 * 1024 * 1024:
        st.error("PDF is too large (maximum 5 MB).")
    else:
        resume_text = extract_pdf_text(uploaded)
        if not resume_text:
            st.error("No selectable text found. Scanned PDFs need OCR (not supported yet).")
        else:
            try:
                with st.spinner("Analyzing with AI..."):
                    analysis = analyze_with_ai(resume_text, job_text)
                    result = calculate_match(analysis["resume_skills"], analysis["required_skills"])
                if result["score"] is None:
                    st.warning("No required skills were extracted; a score cannot be calculated.")
                else:
                    st.metric("Required-skills coverage", f"{result['score']}%")
                    st.write(f"Matched {len(result['matched'])} of {result['total']} required skills")
                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("Matched skills")
                    st.write(", ".join(result["matched"]) or "None identified")
                with c2:
                    st.subheader("Missing / unverified skills")
                    st.write(", ".join(result["missing"]) or "None identified")
                st.subheader("AI recommendations")
                for recommendation in analysis["recommendations"]:
                    st.write("• " + recommendation)
                st.caption("AI may miss skills or infer them incorrectly. Verify all findings against the source documents.")
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
