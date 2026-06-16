# Resumo

**Resumo** is an AI-powered desktop application designed to help job seekers tailor their resumes to specific job descriptions. Built with a sleek PySide6 interface and powered by the blazing-fast Groq API (LLaMA 3), Resumo analyzes your existing resume, compares it against a job description, and intelligently rewrites it to maximize your ATS (Applicant Tracking System) match score.


## Features

- **Smart Analysis:** Instantly compares your resume against a job description to generate a Match Score and highlight missing keywords.
- ** Automated Rewriting:** If your match score is above the threshold (20%), Resumo automatically restructures and rewrites your resume, integrating missing keywords organically without falsifying experience.
- ** Career Assistant Chatbot:** A built-in AI assistant to answer all your career, interview, and recruitment-related questions.
- ** Resume Vault:** Automatically saves all your generated, job-specific resumes to a local MySQL database so you can access them later.
- ** Export to Word:** One-click export of your optimized resume to a fully formatted `.docx` file.
- ** History Tracking:** Keeps track of your past analyses, showing you the companies you applied for and your match scores.
- ** Secure Authentication:** Built-in user authentication with bcrypt password hashing.

##  Tech Stack

- **Frontend:** Python, PySide6 (Qt) for a modern, animated desktop UI.
- **Backend AI:** [Groq API](https://groq.com/) (LLaMA-3 70B) for lightning-fast natural language processing.
- **Database:** MySQL for storing users, chat logs, and the resume vault.
- **File Parsing:** `PyPDF2` and `python-docx` for reading PDFs/Word docs and generating new Word documents.

## Getting Started

### Prerequisites
- Python 3.9+
- MySQL Server installed and running locally
- A free [Groq API Key](https://console.groq.com/keys)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MedBhr-source/Resumo.git
   cd Resumo
   ```

2. **Install dependencies:**
   *(Create a virtual environment if preferred)*
   ```bash
   pip install PySide6 mysql-connector-python bcrypt groq python-dotenv PyPDF2 python-docx
   ```

3. **Set up the Database:**
   - Open your MySQL server.
   - Run the provided SQL script to create the database and tables:
     ```bash
     mysql -u root -p < resume_tailor_db.sql
     ```

4. **Configure Environment Variables:**
   - Copy the example `.env` file to create your own:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and fill in your Groq API key and MySQL password.

5. **Run the App!**
   ```bash
   python main.py
   ```

---
*Built to make the job hunt just a little bit easier.* 
