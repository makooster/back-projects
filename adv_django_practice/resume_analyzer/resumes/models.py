# resumes/models.py
from django.db import models
from django.conf import settings

class Resume(models.Model):
    STATUS_CHOICES = (
        ('uploaded', 'Uploaded'),
        ('processing', 'Processing'),
        ('parsed', 'Parsed'),
        ('error', 'Error'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/')
    extracted_text = models.TextField(blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    score = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume {self.id} - {self.user.username}"
