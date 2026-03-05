# AI Resume Critiquer

AI Resume Critiquer is a **Streamlit-based web application** that analyzes resumes using the **OpenAI API**. Users can upload a **PDF or TXT resume**, optionally enter a **target job title**, and receive structured feedback on resume quality, clarity, skills, and experience to improve job applications.

## Features

- Upload resumes in **PDF or TXT format**
- Automatic **resume text extraction**
- **AI-powered resume analysis**
- Feedback on:
  - Content clarity
  - Skills presentation
  - Experience descriptions
  - Job-specific improvements
- Simple and interactive **Streamlit interface**
  
## Tech Stack

**Frontend**
- Streamlit

**Backend**
- Python

**Libraries**
- PyPDF2
- OpenAI
- python-dotenv
- io
- os

---

## Project Structure

```
AI-Resume-Critiquer
│
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/AI-Resume-Critiquer.git
cd AI-Resume-Critiquer
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory and add your OpenAI API key.

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Running the Application

Run the Streamlit application with:

```bash
streamlit run main.py
```

After running the command, the app will automatically open in your browser.

## How It Works

1. Upload a **resume file (PDF or TXT)**.
2. The app **extracts text from the resume**.
3. Resume content is sent to the **OpenAI API**.
4. The AI analyzes the resume and provides:
   - Content feedback
   - Skill improvement suggestions
   - Experience optimization tips
   - Job-specific recommendations
5. Results are displayed in the **Streamlit interface**.

## Future Improvements

- Resume scoring system
- ATS keyword matching
- AI resume rewriting
- Downloadable feedback report
- Support for DOCX resumes

## License

This project is open source and available under the **MIT License**.
