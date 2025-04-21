# resume_analysis/serializers.py
from rest_framework import serializers
from .models import Resume, ResumeAnalysis, Skill
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

# Pydantic models for validation
class SkillSchema(BaseModel):
    name: str
    category: Optional[str] = None
    proficiency: Optional[float] = None

class EducationSchema(BaseModel):
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class ExperienceSchema(BaseModel):
    company: str
    position: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None

class ResumeDataSchema(BaseModel):
    skills: List[str] = Field(default_factory=list)
    education: List[Dict[str, Any]] = Field(default_factory=list)
    experience: List[Dict[str, Any]] = Field(default_factory=list)
    contact_info: Dict[str, Any] = Field(default_factory=dict)

class AnalysisResultSchema(BaseModel):
    overall_score: float
    strengths: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)
    job_match_score: Optional[float] = None

# Django REST Framework Serializers
class ResumeSerializer(serializers.ModelSerializer):
    """Serializer for Resume model"""
    class Meta:
        model = Resume
        fields = ['id', 'title', 'file', 'file_type', 'uploaded_at', 'user']
        read_only_fields = ['user', 'uploaded_at']
    
    def create(self, validated_data):
        # Assign current user to the resume
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill model"""
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'demand_score']

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for ResumeAnalysis model"""
    class Meta:
        model = ResumeAnalysis
        fields = ['id', 'resume', 'skills', 'experience', 'education', 
                'overall_score', 'strengths', 'improvements', 'analyzed_at']
        read_only_fields = ['resume', 'analyzed_at']

class JobMatchSerializer(serializers.Serializer):
    """Serializer for job matching requests"""
    resume_id = serializers.IntegerField()
    job_description = serializers.CharField()