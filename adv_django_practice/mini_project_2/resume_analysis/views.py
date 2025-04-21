# resume_analysis/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from celery import shared_task
from .models import Resume, ResumeAnalysis, Skill
from .serializers import ResumeSerializer, ResumeAnalysisSerializer, SkillSerializer, JobMatchSerializer
from .services import ResumeParser, ResumeAnalyzer
import json

# Common tech skills for skill extraction
COMMON_SKILLS = [
    'Python', 'JavaScript', 'React', 'Vue.js', 'Angular', 'Django', 'Flask',
    'Express', 'Node.js', 'PHP', 'Laravel', 'SQL', 'PostgreSQL', 'MySQL',
    'MongoDB', 'Firebase', 'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
    'CI/CD', 'Git', 'GitHub', 'GitLab', 'Jira', 'Agile', 'Scrum', 'Java', 
    'C#', 'C++', 'C', 'TypeScript', 'HTML', 'CSS', 'SASS', 'LESS', 'Redux',
    'GraphQL', 'REST API', 'Microservices', 'Machine Learning', 'AI', 'TensorFlow',
    'PyTorch', 'Data Analysis', 'Data Science', 'NLP', 'Computer Vision'
]

@shared_task
def analyze_resume_task(resume_id):
    """Background task to analyze a resume"""
    resume = Resume.objects.get(id=resume_id)
    
    # Parse resume
    parser = ResumeParser(resume.file, resume.file_type)
    resume_data = parser.analyze_resume(COMMON_SKILLS)
    
    # Analyze resume quality
    analyzer = ResumeAnalyzer(resume_data)
    analysis_result = analyzer.analyze_resume_quality()
    
    # Save or update analysis
    analysis, created = ResumeAnalysis.objects.update_or_create(
        resume=resume,
        defaults={
            'skills': resume_data['skills'],
            'experience': resume_data['experience'],
            'education': resume_data['education'],
            'overall_score': analysis_result['overall_score'],
            'strengths': analysis_result['strengths'],
            'improvements': analysis_result['improvements']
        }
    )
    
    # Save extracted skills to the skill database
    for skill_name in resume_data['skills']:
        Skill.objects.get_or_create(name=skill_name)
    
    return analysis.id

class ResumeViewSet(viewsets.ModelViewSet):
    """ViewSet for resume CRUD operations"""
    serializer_class = ResumeSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Return only the current user's resumes
        return Resume.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Save resume and start background analysis
        resume = serializer.save(user=self.request.user)
        analyze_resume_task.delay(resume.id)
    
    @action(detail=True, methods=['get'])
    def analysis(self, request, pk=None):
        """Get resume analysis"""
        resume = self.get_object()
        try:
            analysis = ResumeAnalysis.objects.get(resume=resume)
            serializer = ResumeAnalysisSerializer(analysis)
            return Response(serializer.data)
        except ResumeAnalysis.DoesNotExist:
            return Response(
                {"detail": "Analysis not yet completed. Please try again later."}, 
                status=status.HTTP_202_ACCEPTED
            )
    
    @action(detail=True, methods=['post'])
    def match_job(self, request, pk=None):
        """Match resume with job description"""
        serializer = JobMatchSerializer(data=request.data)
        if serializer.is_valid():
            resume = self.get_object()
            job_description = serializer.validated_data['job_description']
            
            try:
                analysis = ResumeAnalysis.objects.get(resume=resume)
                resume_data = {
                    'skills': analysis.skills,
                    'education': analysis.education,
                    'experience': analysis.experience
                }
                
                analyzer = ResumeAnalyzer(resume_data, job_description)
                match_score = analyzer.match_with_job()
                analysis_result = analyzer.get_full_analysis()
                
                return Response({
                    'match_score': match_score,
                    'analysis': analysis_result
                })
            except ResumeAnalysis.DoesNotExist:
                return Response(
                    {"detail": "Resume analysis not found. Please analyze the resume first."}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for skills"""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending skills based on demand score"""
        top_skills = Skill.objects.order_by('-demand_score')[:20]
        serializer = self.get_serializer(top_skills, many=True)
        return Response(serializer.data)