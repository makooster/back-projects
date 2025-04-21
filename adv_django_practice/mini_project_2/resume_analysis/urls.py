# resume_analysis/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet, SkillViewSet

router = DefaultRouter()
router.register(r'resumes', ResumeViewSet, basename='resume')
router.register(r'skills', SkillViewSet, basename='skill')

urlpatterns = [
    path('', include(router.urls)),
]