# job_matching/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JobListingViewSet,
    JobApplicationViewSet,
    SavedJobViewSet,
    JobSkillTrendViewSet
)

router = DefaultRouter()
router.register(r'listings', JobListingViewSet, basename='job-listing')
router.register(r'applications', JobApplicationViewSet, basename='job-application')
router.register(r'saved', SavedJobViewSet, basename='saved-job')
router.register(r'skill-trends', JobSkillTrendViewSet, basename='skill-trend')

urlpatterns = [
    path('', include(router.urls)),
]