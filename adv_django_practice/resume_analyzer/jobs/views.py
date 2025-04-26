from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from .models import Job
from .serializers import JobSerializer
from resumes.models import Resume
from resumes.serializers import ResumeSerializer
from users.permissions import IsRecruiter

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsRecruiter()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'recruiter':
            return Job.objects.filter(recruiter=user)
        return Job.objects.all()

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

    @action(detail=True, methods=['get'], url_path='match', permission_classes=[permissions.IsAuthenticated, IsRecruiter])
    def match_resumes(self, request, pk=None):
        job = self.get_object()
        cache_key = f'match_results_job_{job.id}'
        cached = cache.get(cache_key)

        if cached:
            return Response(cached, status=status.HTTP_200_OK)

        job_skills = set(job.required_skills)
        matches = []
        for resume in Resume.objects.filter(status='parsed'):
            resume_skills = set(resume.skills)
            match_score = len(job_skills & resume_skills) / max(len(job_skills), 1)
            matches.append({
                'resume': ResumeSerializer(resume).data,
                'score': round(match_score * 100, 2)
            })

        matches.sort(key=lambda x: x['score'], reverse=True)
        cache.set(cache_key, matches, timeout=600)  # Cache for 10 minutes
        return Response(matches, status=status.HTTP_200_OK)