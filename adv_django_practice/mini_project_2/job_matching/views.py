from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q, Count, Avg
from django_filters.rest_framework import DjangoFilterBackend
from .models import JobListing, JobApplication, SavedJob, JobSkillTrend
from .serializers import (
    JobListingSerializer, 
    JobApplicationSerializer, 
    JobApplicationDetailSerializer,
    SavedJobSerializer,
    JobSkillTrendSerializer
)
from resume_analysis.models import ResumeAnalysis
from resume_analysis.services import ResumeAnalyzer
from user_management.models import User

class IsRecruiterOrReadOnly(permissions.BasePermission):
    """Custom permission for recruiters to create/edit jobs"""
    
    def has_permission(self, request, view):
        # Allow read-only access for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        # Allow write access only for recruiters
        return request.user.is_authenticated and request.user.is_recruiter

class IsRecruiter(permissions.BasePermission):
    """Custom permission for recruiters only"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_recruiter

class JobListingViewSet(viewsets.ModelViewSet):
    """ViewSet for job listings"""
    serializer_class = JobListingSerializer
    permission_classes = [IsRecruiterOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['experience_level', 'remote', 'is_active']
    search_fields = ['title', 'description', 'company', 'location', 'required_skills']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_recruiter:
            # Recruiters see only their own job listings by default
            queryset = JobListing.objects.filter(recruiter=self.request.user)
        else:
            # Job seekers see only active job listings
            queryset = JobListing.objects.filter(is_active=True)
            
        # Filter by skills if provided in query params
        skills = self.request.query_params.get('skills', None)
        if skills:
            skill_list = [skill.strip() for skill in skills.split(',')]
            # Filter jobs where any of the required skills match
            for skill in skill_list:
                queryset = queryset.filter(required_skills__contains=[skill])
        
        return queryset
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def match_with_resume(self, request, pk=None):
        """Match a job with the user's resumes"""
        job = self.get_object()
        resume_id = request.query_params.get('resume_id', None)
        
        if resume_id:
            # Match with specific resume
            try:
                analysis = ResumeAnalysis.objects.get(resume__id=resume_id, resume__user=request.user)
                
                # Prepare data for matching
                resume_data = {
                    'skills': analysis.skills,
                    'education': analysis.education,
                    'experience': analysis.experience
                }
                
                job_description = job.description
                required_skills = job.required_skills
                
                # Enrich job description with required skills
                enhanced_job_desc = job_description + "\n\nRequired Skills: " + ", ".join(required_skills)
                
                # Analyze match
                analyzer = ResumeAnalyzer(resume_data, enhanced_job_desc)
                match_score = analyzer.match_with_job()
                analysis_result = analyzer.get_full_analysis()
                
                return Response({
                    'job_id': job.id,
                    'resume_id': int(resume_id),
                    'match_score': match_score,
                    'analysis': analysis_result
                })
            except ResumeAnalysis.DoesNotExist:
                return Response(
                    {"detail": "Resume analysis not found for this resume."}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Return error if no resume specified
            return Response(
                {"detail": "Please specify a resume_id parameter."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'], permission_classes=[IsRecruiter])
    def my_listings(self, request):
        """Get the recruiter's job listings"""
        jobs = JobListing.objects.filter(recruiter=request.user)
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data)

class JobApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for job applications"""
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'list'] and self.request.user.is_recruiter:
            return JobApplicationDetailSerializer
        return JobApplicationSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_recruiter:
            # Recruiters see applications for their jobs
            return JobApplication.objects.filter(job__recruiter=user)
        else:
            # Job seekers see their own applications
            return JobApplication.objects.filter(applicant=user)
    
    def create(self, serializer):
        # Check if user has already applied for this job
        job_id = self.request.data.get('job')
        if JobApplication.objects.filter(job_id=job_id, applicant=self.request.user).exists():
            return Response(
                {"detail": "You have already applied for this job."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the resume and job for matching
        resume_id = self.request.data.get('resume')
        try:
            resume_analysis = ResumeAnalysis.objects.get(resume_id=resume_id)
            job = JobListing.objects.get(pk=job_id)
            
            # Calculate match score
            resume_data = {
                'skills': resume_analysis.skills,
                'education': resume_analysis.education,
                'experience': resume_analysis.experience
            }
            
            enhanced_job_desc = job.description + "\n\nRequired Skills: " + ", ".join(job.required_skills)
            analyzer = ResumeAnalyzer(resume_data, enhanced_job_desc)
            match_score = analyzer.match_with_job()
            
            # Save application with match score
            serializer.save(
                applicant=self.request.user,
                match_score=match_score
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ResumeAnalysis.DoesNotExist, JobListing.DoesNotExist):
            return Response(
                {"detail": "Resume analysis or job not found."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        """Get the user's job applications"""
        applications = JobApplication.objects.filter(applicant=request.user)
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsRecruiter])
    def update_status(self, request, pk=None):
        """Update application status (for recruiters)"""
        application = self.get_object()
        status_value = request.data.get('status')
        
        if not status_value:
            return Response(
                {"detail": "Status value is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate the status value
        valid_statuses = dict(JobApplication._meta.get_field('status').choices).keys()
        if status_value not in valid_statuses:
            return Response(
                {"detail": f"Invalid status. Choose from: {', '.join(valid_statuses)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = status_value
        application.save()
        serializer = self.get_serializer(application)
        return Response(serializer.data)

class SavedJobViewSet(viewsets.ModelViewSet):
    """ViewSet for saved/favorite jobs"""
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user)
    
    def create(self, serializer):
        # Check if job is already saved
        job_id = self.request.data.get('job')
        if SavedJob.objects.filter(job_id=job_id, user=self.request.user).exists():
            return Response(
                {"detail": "You have already saved this job."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class JobSkillTrendViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for job skill trends"""
    queryset = JobSkillTrend.objects.all().order_by('-trending_score')
    serializer_class = JobSkillTrendSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def top_skills(self, request):
        """Get top trending skills"""
        top_skills = JobSkillTrend.objects.all().order_by('-trending_score')[:20]
        serializer = self.get_serializer(top_skills, many=True)
        return Response(serializer.data)