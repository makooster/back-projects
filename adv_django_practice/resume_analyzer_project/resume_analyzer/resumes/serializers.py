from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ['user', 'extracted_text', 'skills', 'education', 'experience', 'score', 'status', 'created_at']
