
import streamlit as st
import pymupdf


st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="🤖",
    layout="wide",
)


def extract_pdf_text(uploaded_file):
    """Extract readable text from a PDF resume."""
    try:
        pdf_bytes = uploaded_file.getvalue()

        with pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        ) as document:
            text = "\n".join(
                page.get_text()
                for page in document
            )

        return text.strip()

    except Exception as error:
        st.error(f"PDF processing failed: {error}")
        return ""


def main():
    st.title("🤖 AI Job Application Assistant")

    st.write(
        "Compare your resume with a job description "
        "and discover opportunities for improvement."
    )

    st.divider()

    resume_col, job_col = st.columns(2)

    with resume_col:
        st.subheader("📄 Your Resume")

        uploaded_file = st.file_uploader(
            "Upload your PDF resume",
            type=["pdf"],
        )

    with job_col:
        st.subheader("💼 Job Description")

        job_description = st.text_area(
            "Paste the job description",
            height=200,
        )

    if st.button("Analyze Resume", type="primary"):

        if uploaded_file is None:
            st.warning("Please upload a PDF resume.")
            return

        if not job_description.strip():
            st.warning("Please enter a job description.")
            return

        resume_text = extract_pdf_text(uploaded_file)

        if not resume_text:
            st.error("No readable resume text found.")
            return

        st.success("Resume processed successfully!")

        st.subheader("Extracted Resume Text")
        st.text_area(
            "Resume content",
            value=resume_text,
            height=250,
        )

        st.subheader("Job Description")
        st.text_area(
            "Job requirements",
            value=job_description,
            height=250,
        )

        st.info(
            "AI-powered analysis will be added "
            "in Lesson 2."
        )


if __name__ == "__main__":
    main()
