# job_matching/models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from resume_analysis.models import Resume

class JobListing(models.Model):
    """Model for job listings"""
    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='job_listings'
    )
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    remote = models.BooleanField(default=False)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    experience_level = models.CharField(
        max_length=20, 
        choices=[
            ('ENTRY', 'Entry Level'),
            ('MID', 'Mid Level'),
            ('SENIOR', 'Senior Level'),
            ('EXECUTIVE', 'Executive')
        ]
    )
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} at {self.company}"

class JobApplication(models.Model):
    """Model for job applications"""
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, related_name='applications')
    cover_letter = models.TextField(blank=True, null=True)
    match_score = models.FloatField(default=0.0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('REVIEWED', 'Reviewed'),
            ('INTERVIEW', 'Interview'),
            ('REJECTED', 'Rejected'),
            ('ACCEPTED', 'Accepted')
        ],
        default='PENDING'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.applicant.username} applied to {self.job.title}"
    
    class Meta:
        unique_together = ('job', 'applicant')

class SavedJob(models.Model):
    """Model for saved/favorite jobs"""
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
    
    class Meta:
        unique_together = ('job', 'user')

class JobSkillTrend(models.Model):
    """Model for tracking trending job skills"""
    skill_name = models.CharField(max_length=100, unique=True)
    frequency = models.IntegerField(default=0)
    trending_score = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.skill_name} - Score: {self.trending_score}"