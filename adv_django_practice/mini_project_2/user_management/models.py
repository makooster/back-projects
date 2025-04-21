# user_management/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser): 
    """Custom user model with additional fields for role-based access"""
    
    class Roles(models.TextChoices):
        JOB_SEEKER = 'SEEKER', _('Job Seeker')
        RECRUITER = 'RECRUITER', _('Recruiter')
        ADMIN = 'ADMIN', _('Admin')
    
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.JOB_SEEKER)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    @property
    def is_job_seeker(self):
        return self.role == self.Roles.JOB_SEEKER
    
    @property
    def is_recruiter(self):
        return self.role == self.Roles.RECRUITER
    
    @property
    def is_admin_user(self):
        return self.role == self.Roles.ADMIN