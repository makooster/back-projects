# feedback/tasks.py
from celery import shared_task
from resumes.models import Resume
from .models import Feedback

TRENDING_SKILLS = {"python", "django", "rest", "sql", "nlp", "aws", "docker"}

@shared_task
def generate_feedback_for_resume(resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
        skills = set(resume.skills)
        skill_gaps = list(TRENDING_SKILLS - skills)

        formatting_tips = "Use consistent headings, bullet points, and avoid dense paragraphs."
        ats_keywords = list(skills)[:5]  

        Feedback.objects.update_or_create(
            resume=resume,
            defaults={
                'skill_gaps': skill_gaps,
                'formatting_tips': formatting_tips,
                'ats_keywords': ats_keywords,
            }
        )
    except Resume.DoesNotExist:
        pass
