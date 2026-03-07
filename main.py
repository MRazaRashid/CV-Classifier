import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI 
from dotenv import load_dotenv

load_dotenv()
# load the enviornment variable from .env file

st.set_page_config(page_title='AI Resume',page_icon='g',layout='centered')
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.title('📄 AI Resume Critiquer')

st.info(
"Upload your resume to receive AI-powered feedback on content clarity, skills, and experience. "
"Optionally add a job title to receive tailored suggestions."
)

OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

upfile=st.file_uploader("Upload your resume", type=["pdf",'txt'])
if upfile:
    st.success("Resume uploaded successfully!")  
jobr=st.text_input("Enetr job title")

anal=st.button("Analayze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)  
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# def extract_text_from_file(upfile):
#     if upfile.type == "application/pdf":
#         return extract_text_from_pdf(io.BytesIO(upfile.read()))
#     return upfile.read().decode("utf-8")     # FIX 1: read once, reuse bytes

def extract_text_from_file(upfile):
    file_bytes = upfile.read()  
    if upfile.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(file_bytes))
    return file_bytes.decode("utf-8")

if anal and upfile:
    try:
        fileContent=extract_text_from_file(upfile)
        if not fileContent.strip():
            st.error("file doesnot exists")
            st.stop()
        st.subheader("📄 Resume Preview")

        st.text_area(
            "Extracted Resume Content",
            fileContent[:2000],height=200)
        prompt = f"""Please analyze this resume and provide constructive feedback
        Focus on the following aspects
        1. Content clarity and impact
        2. skills presentation
        3. experience descriptions
        4. specific improvments for {jobr if jobr else "general job applications"}

        resume content :
        {fileContent}
        please provide your analysis in a clear, structured format with specific reccomendations""" 
        client =OpenAI(api_key=OPENAI_API_KEY)
        with st.spinner("Analyzing your resume..."):  # FIX 3: spinner so you can see AI is working
            response=client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {'role':'system','content':'You are an expert resume reviewer with years of experience in the HR and recruitment'},
                    {'role':'user','content':prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )



        st.subheader("📊 Resume Analysis")
        analysis = response.choices[0].message.content
        st.markdown(analysis)
        st.download_button(label="📥 Download Feedback",
                           data=analysis,
                           file_name="resume_feedback.txt")
    except Exception as e:
        st.error(f"An error occured:{str(e)}")
st.markdown("---")
st.caption("Built with Streamlit and OpenAI • AI Resume Critiquer")
