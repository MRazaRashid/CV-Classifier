import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI 
from dotenv import load_dotenv

load_dotenv()
# load the enviornment variable from .env file

st.set_page_config(page_title='AI Resume',page_icon='g',layout='centered')

st.title('AI Resume Critiquer')
st.markdown("Upload your resume")

OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

upfile=st.file_uploader("Uplooad kr", type=["pdf",'txt'])
   
jobr=st.text_input("enetr job title")

anal=st.button("Analayze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)  
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(upfile):
    if upfile.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(upfile.read()))
    return upfile.read().decode("utf-8")

if anal and upfile:
    try:
        fileContent=extract_text_from_file(upfile)
        if not fileContent.strip():
            st.error("file doesnot exists")
            st.stop
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
        response=client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {'role':'system','content':'You are an expert resume reviewer with years of experience in the HR and recruitment'},
                {'role':'user','content':prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        st.markdown("### Analysis Results")
        st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"An error occured:{str(e)}")






















# import streamlit as st
# import io                          
# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# # ────────────────────────────────────────────────
# #  Load environment variables
# # ────────────────────────────────────────────────
# load_dotenv()

# if not os.getenv("OPENAI_API_KEY"):
#     st.error("OPENAI_API_KEY not found in .env file")
#     st.stop()

# client = OpenAI()

# # ────────────────────────────────────────────────
# #  Page config
# # ────────────────────────────────────────────────
# st.set_page_config(
#     page_title="AI Resume Critiquer",
#     page_icon="📄",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # ────────────────────────────────────────────────
# #  Some dark-theme friendly styling
# # ────────────────────────────────────────────────
# st.markdown("""
#     <style>
#     .main .block-container {
#         max-width: 720px;
#         padding-top: 2rem;
#         padding-bottom: 5rem;
#     }
#     .stButton > button {
#         width: 100%;
#         height: 3.4rem;
#         font-size: 1.2rem;
#         margin-top: 1.8rem;
#     }
#     div[data-testid="stFileUploader"] {
#         border: 2px dashed #4a5568;
#         border-radius: 12px;
#         padding: 3.5rem 1.5rem;
#         background: #1a202c;
#         text-align: center;
#     }
#     div[data-testid="stFileUploader"]::before {
#         content: "📤";
#         font-size: 4rem;
#         margin-bottom: 1.2rem;
#         display: block;
#     }
#     div[data-testid="stFileUploader"] label {
#         font-size: 1.3rem !important;
#         color: #e2e8f0 !important;
#     }
#     .upload-hint {
#         font-size: 0.95rem;
#         color: #94a3b8;
#         text-align: center;
#         margin-top: 0.8rem;
#     }
#     h1 {
#         text-align: center;
#         margin-bottom: 0.6rem;
#     }
#     .subtitle {
#         text-align: center;
#         color: #cbd5e0;
#         margin-bottom: 2.8rem;
#         font-size: 1.18rem;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # ────────────────────────────────────────────────
# #  UI
# # ────────────────────────────────────────────────
# st.title("AI Resume Critiquer")

# st.markdown(
#     '<div class="subtitle">'
#     'Upload your resume and get AI-powered feedback tailored to your needs!'
#     '</div>',
#     unsafe_allow_html=True
# )

# # File uploader
# uploaded_file = st.file_uploader(
#     "",
#     type=["pdf", "txt"],
#     accept_multiple_files=False,
#     help="PDF or TXT • max 200MB",
#     label_visibility="collapsed"
# )

# if uploaded_file is not None:
#     file_size_mb = uploaded_file.size / (1024 * 1024)
#     st.caption(f"**{uploaded_file.name}** selected  •  {file_size_mb:.1f} MB")

# # Job role input
# job_role = st.text_input(
#     "Enter the job role you're targeting (optional)",
#     placeholder="e.g. Senior Full-Stack Engineer, Product Manager, Data Scientist",
#     label_visibility="visible"
# )

# # Analyze button
# if st.button("Analyze Resume", type="primary", use_container_width=True, disabled=uploaded_file is None):
#     if not uploaded_file:
#         st.warning("Please upload your resume first.")
#         st.stop()

#     with st.spinner("Reading file and analyzing with AI..."):
#         try:
#             # ─── Read file content ──────────────────────────────
#             file_bytes = uploaded_file.read()
#             content = ""

#             if uploaded_file.type == "application/pdf":
#                 try:
#                     from pypdf import PdfReader
#                     pdf = PdfReader(io.BytesIO(file_bytes))
#                     content = "\n".join(page.extract_text() or "" for page in pdf.pages)
#                 except Exception as e:
#                     st.error(f"Could not read PDF → {str(e)}")
#                     st.stop()
#             else:
#                 # plain text
#                 try:
#                     content = file_bytes.decode("utf-8", errors="replace")
#                 except:
#                     st.error("Could not decode text file.")
#                     st.stop()

#             if len(content.strip()) < 40:
#                 st.warning("The uploaded file seems empty or could not be parsed properly.")
#                 st.stop()

#             # ─── Prepare prompt ─────────────────────────────────
#             target_role = job_role.strip() if job_role.strip() else "general professional / software engineering role"

#             prompt = f"""You are an expert resume reviewer and career coach with 15+ years of recruiting and hiring experience.
# You give honest, constructive, specific, detailed and actionable feedback.

# Job role the candidate is targeting: {target_role}

# Resume content:
# ----------------------------------------
# {content[:16500]}   <!-- truncate very long resumes -->
# ----------------------------------------

# Provide feedback using this exact structure (use markdown):

# ### 1. Overall Impression
# (2–4 sentences summary)

# ### 2. Strengths
# - bullet points

# ### 3. Areas for Improvement
# - bullet points with clear explanations

# ### 4. Specific Phrasing / Wording Suggestions
# Give 4–7 concrete before → after examples

# ### 5. Formatting & Structure Recommendations

# ### 6. ATS-Friendliness Notes
# (especially keywords, sections, fonts, etc.)

# ### 7. Current Version Score
# X/10  (be honest and explain briefly)

# Be professional, encouraging but direct. Use clear markdown formatting."""

#             # ─── Call OpenAI ────────────────────────────────────
#             response = client.chat.completions.create(
#                 model="gpt-4o-mini",          # ← change to gpt-4o or gpt-4-turbo if you prefer & can afford
#                 messages=[
#                     {"role": "system", "content": "You are a world-class technical resume consultant and former FAANG recruiter."},
#                     {"role": "user",   "content": prompt}
#                 ],
#                 temperature=0.65,
#                 max_tokens=2200
#             )

#             feedback = response.choices[0].message.content

#             # ─── Display result ─────────────────────────────────
#             st.subheader("AI Resume Feedback")
#             st.markdown(feedback)

#         except Exception as e:
#             st.error(f"Analysis failed.\n{str(e)}")

# # Small hint when no file is uploaded
# if not uploaded_file:
#     st.markdown(
#         '<div class="upload-hint">PDF or TXT files supported • max 200 MB</div>',
#         unsafe_allow_html=True
#     )