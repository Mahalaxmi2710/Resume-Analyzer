# Resume Analyzer 📝🔍  

## Overview  
The **Resume Analyzer** is a web-based application that helps job seekers evaluate how well their resumes match specific job roles. It extracts text from uploaded resumes, analyzes required skills, and provides a **Job Fit Score** along with missing and matched skills.  

## Features  
- 📂 **Upload Resume (PDF Format Only)**  
- 🛠 **Skill Matching Against Job Roles**  
- 📊 **Job Fit Score Calculation**  
- 🎯 **Highlights Matched & Missing Skills**  
- ⚡ **Fast & Lightweight (Powered by FastAPI & JavaScript)**  

## Tech Stack  
- **Backend:** FastAPI, SQLite, pdfplumber  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** SQLite  

## Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/Mahalaxmi2710/resume-analyzer.git
cd resume-analyzer
```

### 2️⃣ Install Python Dependencies 
Ensure you have Python installed, then install the required dependencies:
```bash
pip install fastapi uvicorn pdfplumber sqlite3
```
### 3️⃣ Run the Backend Server
Start the FastAPI server:
```bash
uvicorn main:app --reload
```
(Ensure main.py is the correct filename for your backend script.)

### 4️⃣ Run the Frontend
Simply open index.html in a browser.

### API Endpoint
POST /analyze/ → Accepts a resume file and job role, then returns:
- matched_skills: List of skills found in the resume
- missing_skills: List of skills required but missing
- job_fit_score: Percentage of match


