# resumes/tasks.py
import os
from celery import shared_task
from .models import Resume
import fitz  # PyMuPDF
import spacy
from feedback.tasks import generate_feedback_for_resume

nlp = spacy.load("en_core_web_sm")

@shared_task
def parse_resume_file(resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
        file_path = resume.file.path

        text = ""
        if file_path.endswith(".pdf"):
            with fitz.open(file_path) as doc:
                text = " ".join([page.get_text() for page in doc])

        resume.extracted_text = text
        doc = nlp(text)
        skills = [ent.text.lower() for ent in doc.ents if ent.label_ == "SKILL"]
        resume.skills = list(set(skills))
        resume.status = 'parsed'
        resume.save()

        generate_feedback_for_resume.delay(resume.id)

    except Exception as e:
        resume.status = 'error'
        resume.save()
