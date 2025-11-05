import sqlite3
from fastapi import FastAPI, File, UploadFile, Form
import pdfplumber
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
conn = sqlite3.connect("resumes.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    content TEXT,
    profession TEXT,
    skills TEXT
)
""")
conn.commit()

# Required skills mapping
required_skills = {
    "Software Developer": ["Python", "JavaScript", "Java", "C++", "React", "Node.js", "Flask", "Django", "PostgreSQL", "AWS"],
    "Data Scientist": ["Python", "R", "SQL", "TensorFlow", "Scikit-Learn", "Data Visualization", "Statistics", "Machine Learning"],
    "UI/UX Designer": ["Adobe XD", "Figma", "Sketch", "HTML", "CSS", "User Research", "Wireframing"],
    "Cybersecurity Analyst": ["Network Security", "Penetration Testing", "Encryption", "Firewalls", "SIEM", "Incident Response"],
    "DevOps Engineer": ["Docker", "Kubernetes", "Jenkins", "Terraform", "AWS", "CI/CD", "Linux", "Bash"],
    "Project Manager": ["Agile", "Scrum", "Kanban", "Stakeholder Management", "Risk Management", "Budgeting"],
    "Business Analyst": ["SQL", "Excel", "Power BI", "Tableau", "Data Modeling", "Requirement Analysis"],
    "Cloud Engineer": ["AWS", "Azure", "Google Cloud", "Terraform", "Serverless Computing", "Networking"],
    "Embedded Systems Engineer": ["C", "C++", "Microcontrollers", "RTOS", "PCB Design", "IoT"],
    "AI/ML Engineer": ["Deep Learning", "NLP", "Computer Vision", "PyTorch", "Keras", "Big Data"],
    "Network Engineer": ["Cisco", "Routing", "Switching", "LAN", "WAN", "BGP", "VPN", "Firewall"],
    "Database Administrator": ["MySQL", "PostgreSQL", "MongoDB", "Oracle", "SQL Server", "Backup & Recovery"],
    "Quality Assurance Engineer": ["Selenium", "JIRA", "Test Automation", "Regression Testing", "Bug Tracking"],
    "Full Stack Developer": ["React", "Angular", "Vue.js", "Node.js", "Express", "MongoDB", "GraphQL"],
    "Game Developer": ["Unity", "Unreal Engine", "C#", "C++", "Game Physics", "3D Modeling"]
}

# Function to extract text from PDF
def extract_text_from_pdf(file: UploadFile) -> str:
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text.strip()

# Function to generate improvement suggestions
def generate_suggestions(missing_skills):
    suggestions = []
    for skill in missing_skills:
        suggestions.append(f"Consider learning {skill} through online courses, projects, or certifications.")
    return suggestions

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze/")
async def analyze_resume(resume: UploadFile = File(...), job_role: str = Form(...)):
    resume_text = extract_text_from_pdf(resume)
    extracted_skills = [skill for skill in required_skills.get(job_role, []) if skill.lower() in resume_text.lower()]
    missing_skills = set(required_skills.get(job_role, [])) - set(extracted_skills)
    total_skills = len(required_skills.get(job_role, []))
    job_fit_score = (len(extracted_skills) / total_skills) * 100 if total_skills else 0

    suggestions = generate_suggestions(missing_skills)

    cursor.execute("INSERT INTO resumes (filename, content, profession, skills) VALUES (?, ?, ?, ?)",
                   (resume.filename, resume_text, job_role, ', '.join(extracted_skills)))
    conn.commit()

    return {
        "matched_skills": extracted_skills,
        "missing_skills": list(missing_skills),
        "job_fit_score": round(job_fit_score, 2),
        "suggestions": suggestions
    }
