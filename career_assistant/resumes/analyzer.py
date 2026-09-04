
import re

TECHNICAL_SKILLS = [
    "python", "java", "javascript", "c++", "c#", "sql", "html", "css",
    "react", "angular", "vue", "node.js", "django", "flask", "spring",
    "machine learning", "deep learning", "data science", "artificial intelligence",
    "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "linux",
    "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
    "rest api", "graphql", "microservices", "ci/cd", "devops",
    "typescript", "php", "ruby", "swift", "kotlin", "go", "rust",
    "tableau", "power bi", "excel", "r", "matlab", "sas",
    "selenium", "jenkins", "terraform", "ansible",
]

SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "problem solving",
    "critical thinking", "time management", "adaptability", "creativity",
    "project management", "agile", "scrum",
]

EDUCATION_KEYWORDS = [
    "b.tech", "btech", "b.e", "m.tech", "mtech", "m.e", "mba", "bba",
    "b.sc", "bsc", "m.sc", "msc", "b.com", "bcom", "m.com",
    "phd", "doctorate", "bachelor", "master", "degree", "diploma",
    "intermediate", "12th", "10th", "certification", "certified",
    "bca", "mca", "b.a", "m.a",
]

EXPERIENCE_KEYWORDS = [
    "internship", "intern", "worked", "working", "experience",
    "years", "months", "project", "developed", "managed", "led",
    "designed", "implemented", "built", "created", "responsible",
    "contributed", "collaborated", "analyzed", "optimized",
]


def extract_text_from_pdf(file_path):
    try:
        import PyPDF2
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception:
        return ""


def extract_text_from_docx(file_path):
    try:
        import docx
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        return ""


def extract_text(file_path):
    path_lower = str(file_path).lower()
    if path_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif path_lower.endswith(".docx"):
        return extract_text_from_docx(file_path)
    return ""


def analyze_resume(file_path):
    text = extract_text(file_path)
    if not text:
        return {
            "extracted_text": "",
            "resume_score": 0,
            "detected_skills": [],
            "missing_skills": list(TECHNICAL_SKILLS[:10]),
            "detected_education": [],
            "detected_experience": [],
            "suggestions": ["Could not extract text from the resume. Please upload a valid PDF or DOCX file."],
            "formatting_score": 0,
        }

    text_lower = text.lower()

    # Detect skills
    found_technical = [s for s in TECHNICAL_SKILLS if s.lower() in text_lower]
    found_soft = [s for s in SOFT_SKILLS if s.lower() in text_lower]
    all_found = found_technical + found_soft
    missing = [s for s in TECHNICAL_SKILLS[:15] if s.lower() not in text_lower]

    # Detect education
    found_education = list(set(
        kw for kw in EDUCATION_KEYWORDS if kw.lower() in text_lower
    ))

    # Detect experience
    found_experience = list(set(
        kw for kw in EXPERIENCE_KEYWORDS if kw.lower() in text_lower
    ))

    # Scoring
    skill_score = min(35, len(found_technical) * 3 + len(found_soft) * 2)
    edu_score = min(20, len(found_education) * 5)
    exp_score = min(20, len(found_experience) * 3)

    word_count = len(text.split())
    length_score = 10 if 200 <= word_count <= 1000 else (7 if word_count > 1000 else 3)

    has_email = bool(re.search(r'[\w.-]+@[\w.-]+', text))
    has_phone = bool(re.search(r'[\+]?[\d\s\-]{10,}', text))
    has_sections = sum(1 for kw in ["education", "experience", "skills", "projects", "summary", "objective"]
                       if kw in text_lower)
    fmt_score = min(15, (5 if has_email else 0) + (3 if has_phone else 0) + has_sections * 2)

    total = skill_score + edu_score + exp_score + length_score + fmt_score

    # Suggestions
    suggestions = []
    if len(found_technical) < 5:
        suggestions.append("Add more technical skills relevant to your target role")
    if not found_education:
        suggestions.append("Include your educational qualifications clearly")
    if not found_experience:
        suggestions.append("Add work experience or internship details")
    if not has_email:
        suggestions.append("Add a professional email address")
    if not has_phone:
        suggestions.append("Include a contact phone number")
    if has_sections < 3:
        suggestions.append("Use clear section headers like Education, Experience, Skills, Projects")
    if word_count < 200:
        suggestions.append("Your resume is too short — aim for 300-700 words")
    if word_count > 1000:
        suggestions.append("Consider making your resume more concise")
    if len(found_soft) < 2:
        suggestions.append("Highlight soft skills like leadership, teamwork, and communication")
    if not suggestions:
        suggestions.append("Great resume! Keep it updated with your latest accomplishments")

    return {
        "extracted_text": text,
        "resume_score": total,
        "detected_skills": all_found,
        "missing_skills": missing,
        "detected_education": found_education,
        "detected_experience": found_experience,
        "suggestions": suggestions,
        "formatting_score": fmt_score,
    }
