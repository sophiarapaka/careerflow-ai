# CareerFlow AI

> Intelligent Career & Recruitment Automation Platform

CareerFlow AI is a Django-based platform that helps job seekers optimize resumes, discover relevant job opportunities, receive personalized certification recommendations, and follow structured learning pathways. It also enables recruiters to manage job postings, review candidates, and streamline hiring workflows.

## Features

* Resume upload and analysis
* Skill extraction and resume scoring
* Job matching based on skills
* Personalized certification recommendations
* Learning pathways
* Recruiter dashboard
* Job posting and application tracking

## Tech Stack

* Python
* Django
* HTML
* CSS
* JavaScript
* SQLite

## Installation

```bash
git clone https://github.com/sophiarapaka/careerflow-ai.git
cd careerflow-ai
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Future Enhancements

* AI interview preparation
* ATS resume optimization
* Real-time job recommendations
* Email notifications
* Analytics dashboard

  ## Installation & Setup

Follow these steps to run the project locally.

### Clone the repository

```bash
git clone https://github.com/sophiarapaka/careerflow-ai.git
cd careerflow-ai
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py makemigrations accounts jobs resumes
python manage.py migrate
```

### Load sample job data

```bash
python manage.py load_sample_jobs
```

### Create an admin account

```bash
python manage.py createsuperuser
```

### Run the development server

```bash
python manage.py runserver
```

Open your browser and visit:

`http://127.0.0.1:8000/`

