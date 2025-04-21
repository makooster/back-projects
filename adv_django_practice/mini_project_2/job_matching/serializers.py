# job_matching/serializers.py
from rest_framework import serializers
from django.db.models import Avg
from .models import JobListing, JobApplication, SavedJob, JobSkillTrend
from user_management.serializers import UserSerializer
from resume_analysis.serializers import ResumeSerializer

class JobListingSerializer(serializers.ModelSerializer):
    """Serializer for job listings"""
    recruiter_name = serializers.CharField(source='recruiter.username', read_only=True)
    company_name = serializers.CharField(source='recruiter.company_name', read_only=True)
    applications_count = serializers.SerializerMethodField()
    
    class Meta:
        model = JobListing
        fields = ['id', 'title', 'company', 'location', 'remote', 'description',
                 'required_skills', 'experience_level', 'salary_min', 'salary_max',
                 'created_at', 'updated_at', 'is_active', 'recruiter', 'recruiter_name',
                 'company_name', 'applications_count']
        read_only_fields = ['recruiter', 'created_at', 'updated_at', 'applications_count']
    
    def get_applications_count(self, obj):
        return obj.applications.count()
    
    def create(self, validated_data):
        # Set the recruiter to the current user
        validated_data['recruiter'] = self.context['request'].user
        return super().create(validated_data)

class JobApplicationSerializer(serializers.ModelSerializer):
    """Serializer for job applications"""
    applicant_name = serializers.CharField(source='applicant.username', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.company', read_only=True)
    resume_title = serializers.CharField(source='resume.title', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'applicant', 'applicant_name', 'resume', 'resume_title',
                 'job_title', 'company_name', 'cover_letter', 'match_score', 'status',
                 'applied_at', 'updated_at']
        read_only_fields = ['applicant', 'applied_at', 'updated_at', 'match_score']
    
    def create(self, validated_data):
        # Set the applicant to the current user
        validated_data['applicant'] = self.context['request'].user
        return super().create(validated_data)

class JobApplicationDetailSerializer(JobApplicationSerializer):
    """Detailed serializer for job applications with resume info"""
    applicant = UserSerializer(read_only=True)
    resume = ResumeSerializer(read_only=True)

class SavedJobSerializer(serializers.ModelSerializer):
    """Serializer for saved jobs"""
    job_details = JobListingSerializer(source='job', read_only=True)
    
    class Meta:
        model = SavedJob
        fields = ['id', 'job', 'job_details', 'user', 'saved_at']
        read_only_fields = ['user', 'saved_at']
    
    def create(self, validated_data):
        # Set the user to the current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class JobSkillTrendSerializer(serializers.ModelSerializer):
    """Serializer for job skill trends"""
    class Meta:
        model = JobSkillTrend
        fields = ['id', 'skill_name', 'frequency', 'trending_score', 'updated_at']
        read_only_fields = ['frequency', 'trending_score', 'updated_at']