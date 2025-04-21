from django.contrib import admin
from .models import Resume, ResumeAnalysis, Skill, UserActivity
# Register your models here.

admin.site.register(Resume)
admin.site.register(ResumeAnalysis)
admin.site.register(Skill)
admin.site.register(UserActivity)