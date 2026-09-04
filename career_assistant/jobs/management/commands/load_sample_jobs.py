
from django.core.management.base import BaseCommand
from jobs.models import Job

SAMPLE_JOBS = [
    {"title": "Python Developer", "company": "TCS", "location": "Hyderabad", "salary": "6-10 LPA",
     "job_type": "full-time", "experience": "1-3 years",
     "description": "We are looking for a skilled Python Developer to join our team. You will work on building scalable web applications and APIs using Django and Flask frameworks.",
     "requirements": "Strong Python fundamentals, experience with Django or Flask, knowledge of SQL databases, Git version control.",
     "skills": "Python, Django, Flask, SQL, Git, REST API, Linux"},
    {"title": "Frontend Developer", "company": "Infosys", "location": "Bangalore", "salary": "5-8 LPA",
     "job_type": "full-time", "experience": "0-2 years",
     "description": "Join our frontend team to build modern, responsive web applications. You will collaborate with designers and backend developers to deliver exceptional user experiences.",
     "requirements": "Proficiency in HTML, CSS, JavaScript. Experience with React or Angular. Understanding of responsive design.",
     "skills": "HTML, CSS, JavaScript, React, TypeScript, Git, Node.js"},
    {"title": "Data Scientist", "company": "Wipro", "location": "Pune", "salary": "8-15 LPA",
     "job_type": "full-time", "experience": "2-5 years",
     "description": "Seeking a Data Scientist to analyze large datasets, build predictive models, and deliver actionable insights for business decisions.",
     "requirements": "Strong statistics background, experience with ML frameworks, proficiency in Python and SQL.",
     "skills": "Python, Machine Learning, Deep Learning, SQL, TensorFlow, Pandas, NumPy, Scikit-learn, Tableau"},
    {"title": "DevOps Engineer", "company": "Amazon", "location": "Hyderabad", "salary": "12-20 LPA",
     "job_type": "full-time", "experience": "3-5 years",
     "description": "We need a DevOps Engineer to manage cloud infrastructure, implement CI/CD pipelines, and ensure high availability of our services.",
     "requirements": "Experience with AWS services, Docker, Kubernetes, CI/CD tools, and Infrastructure as Code.",
     "skills": "AWS, Docker, Kubernetes, Jenkins, Terraform, Linux, Git, CI/CD, Python"},
    {"title": "Java Developer", "company": "HCL Technologies", "location": "Noida", "salary": "7-12 LPA",
     "job_type": "full-time", "experience": "2-4 years",
     "description": "Looking for an experienced Java Developer to design and develop enterprise-grade applications using Spring Boot and microservices architecture.",
     "requirements": "Strong Java skills, Spring Boot experience, knowledge of microservices, SQL and NoSQL databases.",
     "skills": "Java, Spring, Microservices, SQL, MongoDB, Git, REST API, Docker"},
    {"title": "ML Engineer Intern", "company": "Flipkart", "location": "Bangalore", "salary": "25K-40K/month",
     "job_type": "internship", "experience": "0-1 years",
     "description": "Exciting internship opportunity to work on real-world machine learning projects. You will assist in building and deploying ML models at scale.",
     "requirements": "Basic understanding of ML algorithms, Python programming, willingness to learn.",
     "skills": "Python, Machine Learning, NumPy, Pandas, Scikit-learn"},
    {"title": "Full Stack Developer", "company": "Zoho", "location": "Chennai", "salary": "6-11 LPA",
     "job_type": "full-time", "experience": "1-3 years",
     "description": "We are hiring Full Stack Developers to build end-to-end web applications. You will work on both frontend and backend using modern technologies.",
     "requirements": "Experience with JavaScript/TypeScript, React or Vue, Node.js or Django, SQL databases.",
     "skills": "JavaScript, React, Node.js, Python, Django, SQL, MongoDB, HTML, CSS, Git"},
    {"title": "Cloud Solutions Architect", "company": "Microsoft", "location": "Hyderabad", "salary": "18-30 LPA",
     "job_type": "full-time", "experience": "5-8 years",
     "description": "Design and implement cloud solutions on Azure for enterprise clients. Lead technical discussions and provide architectural guidance.",
     "requirements": "Deep knowledge of Azure services, cloud architecture patterns, networking, security best practices.",
     "skills": "Azure, AWS, Docker, Kubernetes, Terraform, Python, Microservices, DevOps, CI/CD"},
    {"title": "UI/UX Designer", "company": "Swiggy", "location": "Bangalore", "salary": "8-14 LPA",
     "job_type": "remote", "experience": "2-4 years",
     "description": "Create beautiful and intuitive user interfaces for our mobile and web applications. Conduct user research and translate insights into designs.",
     "requirements": "Proficiency in Figma/Sketch, understanding of design systems, experience with user research.",
     "skills": "HTML, CSS, JavaScript, React"},
    {"title": "Cybersecurity Analyst", "company": "Deloitte", "location": "Mumbai", "salary": "10-16 LPA",
     "job_type": "full-time", "experience": "2-5 years",
     "description": "Monitor and protect organizational assets from cyber threats. Conduct vulnerability assessments and implement security measures.",
     "requirements": "Knowledge of security frameworks, experience with SIEM tools, networking fundamentals.",
     "skills": "Linux, Python, SQL, Git"},
]

class Command(BaseCommand):
    help = "Load sample job listings"

    def handle(self, *args, **kwargs):
        for data in SAMPLE_JOBS:
            Job.objects.get_or_create(title=data["title"], company=data["company"], defaults=data)
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(SAMPLE_JOBS)} sample jobs."))
