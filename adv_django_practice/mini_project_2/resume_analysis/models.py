# resume_analysis/models.py
from django.db import models 
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Resume(models.Model):
    """Model for storing resume files and metadata"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resumes/')
    file_type = models.CharField(max_length=10, choices=[('PDF', 'PDF'), ('DOCX', 'DOCX')])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Resume - {self.title}"
    
    class Meta:
        app_label = 'resume_analysis'
        managed = False

class ResumeAnalysis(models.Model):
    """Model for storing AI analysis results of resumes"""
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='analysis')
    skills = models.JSONField(default=dict)
    experience = models.JSONField(default=dict)
    education = models.JSONField(default=dict)
    overall_score = models.FloatField(default=0.0)
    strengths = models.JSONField(default=list)
    improvements = models.JSONField(default=list)
    analyzed_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analysis for {self.resume.title}"
    
    class Meta:
        app_label = 'resume_analysis'
        verbose_name_plural = 'Resume Analyses'
        managed = False

class Skill(models.Model):
    """Model for storing skills extracted from resumes"""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    demand_score = models.FloatField(default=0.0)  # Based on job market trends
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'resume_analysis'
        managed = False

class UserActivity(models.Model):
    """Model for logging user activities"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.created_at}"
    
    class Meta:
        app_label = 'user_activity'
        verbose_name_plural = 'User Activities'
        managed = False