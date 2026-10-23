
import streamlit as st
import pymupdf

from gemini_analyzer import analyze_resume


# Configure Streamlit page
st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="🤖",
    layout="wide"
)


def extract_pdf_text(uploaded_file):
    """Extract text from an uploaded PDF resume."""

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
        "Analyze your resume against a job description "
        "using Google Gemini AI."
    )

    st.divider()

    # Create two columns
    col1, col2 = st.columns(2)

    # Resume upload
    with col1:

        st.subheader("📄 Upload Your Resume")

        uploaded_file = st.file_uploader(
            "Choose a PDF resume",
            type=["pdf"]
        )

    # Job description input
    with col2:

        st.subheader("💼 Job Description")

        job_description = st.text_area(
            "Paste the job description",
            height=250,
            placeholder="Enter job requirements here..."
        )

    st.divider()

    # Analyze button
    if st.button("Analyze Resume", type="primary"):

        if uploaded_file is None:
            st.warning("Please upload your resume.")
            return

        if not job_description.strip():
            st.warning("Please enter a job description.")
            return

        # Extract resume text
        resume_text = extract_pdf_text(uploaded_file)

        if not resume_text:
            st.error("No readable text found in the PDF.")
            return

        # Call Gemini AI
        try:

            with st.spinner("Analyzing resume with Gemini AI..."):

                result = analyze_resume(
                    resume_text,
                    job_description
                )

            st.success("AI analysis completed successfully!")

            # Match score
            st.subheader("📊 Resume Match Score")

            st.metric(
                "Skills Match",
                f"{result['match_score']}%"
            )

            st.progress(
                result["match_score"] / 100
            )

            # Matched skills
            st.subheader("✅ Matched Skills")

            if result["matched_skills"]:

                for skill in result["matched_skills"]:
                    st.success(skill)

            else:
                st.info("No matching skills identified.")

            # Missing skills
            st.subheader("⚠️ Missing Skills")

            if result["missing_skills"]:

                for skill in result["missing_skills"]:
                    st.warning(skill)

            else:
                st.info("No missing skills identified.")

            # Recommendations
            st.subheader("💡 AI Recommendations")

            for recommendation in result["recommendations"]:
                st.write(f"• {recommendation}")

        except Exception as error:

            st.error(f"Analysis failed: {error}")


if __name__ == "__main__":
    main()
