"""Streamlit front end for evidence-based AI resume analysis."""
import streamlit as st
import pymupdf
from src.gemini_analyzer import analyze_resume

st.set_page_config(page_title="AI Job Application Assistant", page_icon="🤖", layout="wide")


def extract_pdf_text(uploaded_file):
    with pymupdf.open(stream=uploaded_file.getvalue(), filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc).strip()


def main():
    st.title("🤖 AI Job Application Assistant")
    st.caption("Lesson 3: evidence-based skill matching and weighted scoring")
    left, right = st.columns(2)
    with left:
        uploaded_file = st.file_uploader("Upload a PDF resume", type=["pdf"])
    with right:
        job_description = st.text_area("Paste the job description", height=220)

    if st.button("Analyze Resume", type="primary"):
        if uploaded_file is None or not job_description.strip():
            st.warning("Please upload a resume and enter a job description.")
            return
        try:
            resume_text = extract_pdf_text(uploaded_file)
            if not resume_text:
                st.error("No readable text found. Scanned PDFs may require OCR.")
                return
            with st.spinner("Analyzing job requirements and resume evidence..."):
                result = analyze_resume(resume_text, job_description)
        except Exception as exc:
            st.error(f"Analysis failed: {exc}")
            return
        st.success("Analysis completed")
        st.metric("Weighted skills coverage", f"{result['match_score']:.1f}%")
        st.progress(result["match_score"] / 100)
        st.caption("Required skills count twice as much as preferred skills. Not a hiring prediction.")
        required = [r for r in result["requirements"] if r["importance"] == "required"]
        preferred = [r for r in result["requirements"] if r["importance"] == "preferred"]
        for heading, items in [("Required skills", required), ("Preferred skills", preferred)]:
            st.subheader(heading)
            if not items:
                st.info("No requirements identified in this category.")
            for item in items:
                if item["matched"]:
                    st.success(f"Matched: {item['skill']}")
                    st.caption(f"Resume evidence: {item['evidence']}")
                else:
                    st.warning(f"Not demonstrated: {item['skill']}")
        st.subheader("Recommendations")
        for suggestion in result["recommendations"]:
            st.write(f"• {suggestion}")


if __name__ == "__main__":
    main()
