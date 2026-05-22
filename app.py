import streamlit as st
from google import genai
import PyPDF2

# ----------------------------
# Configure Gemini API
# ----------------------------

client = genai.Client(
    api_key="YOUR_API_KEY"
)

# ----------------------------
# Streamlit UI
# ----------------------------

st.title("AI Resume Analyzer")

st.write("Upload your resume and get AI-powered analysis")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# ----------------------------
# When Resume Uploaded
# ----------------------------

if uploaded_file is not None:

    # Read PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    resume_text = ""

    for page in pdf_reader.pages:
        extracted = page.extract_text()

        if extracted:
            resume_text += extracted

    st.success("Resume uploaded successfully!")

    # ----------------------------
    # AI Prompt
    # ----------------------------

    prompt = f"""
    Analyze this resume.

    Give:
    1. ATS Score
    2. Skills
    3. Missing Keywords
    4. 3 Improvements
    5. 3 Interview Questions

    Resume:
    {resume_text[:1500]}
    """

    # ----------------------------
    # Generate AI Response
    # ----------------------------

    with st.spinner("Analyzing Resume..."):

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            result = response.text

        except Exception as e:
            result = f"Error: {str(e)}"

            st.subheader("AI Resume Analysis")

            st.write(result)

            st.download_button(
                "Download Analysis",
                result,
                file_name="resume_analysis.txt"
            )


        except Exception as e:

            st.error("API quota exceeded. Please wait a minute and try again.")

            st.stop()