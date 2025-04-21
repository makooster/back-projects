from django.contrib import admin
from .models import JobApplication, JobListing, JobSkillTrend, SavedJob
# Register your models here.
admin.site.register(JobApplication)
admin.site.register(JobListing)
admin.site.register(JobSkillTrend)
admin.site.register(SavedJob)