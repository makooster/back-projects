from django.db import models
from resumes.models import Resume

class Feedback(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='feedback')
    skill_gaps = models.JSONField(default=list, blank=True)
    formatting_tips = models.TextField(blank=True, null=True)
    ats_keywords = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Resume {self.resume.id}"
