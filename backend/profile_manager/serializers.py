from rest_framework import serializers
from .models import Profile, ProfileData, TechStack, Career, AcademicRecord, Certificate, Language

class ProfileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileData
        fields = ['profile', 'original_data', 'processed_data', 'pdf_data']

class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = ['profile', 'tech_stack_name']

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['profile', 'company_name', 'position', 'responsibilities', 'start_date', 'end_date', 'is_currently_employed', 'description']

class AcademicRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicRecord
        fields = ['profile', 'school_name', 'major', 'status', 'enrollment_date', 'graduation_date']

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['profile', 'name']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['profile', 'language_name', 'description']

class ProfileSerializer(serializers.ModelSerializer):
    profile_data = ProfileDataSerializer()
    tech_stacks = TechStackSerializer(many=True)
    careers = CareerSerializer(many=True)
    academic_records = AcademicRecordSerializer(many=True)
    certificates = CertificateSerializer(many=True)
    languages = LanguageSerializer(many=True)

    class Meta:
        model = Profile
        fields = [
            'profile_id', 
            'name', 'job_category', 
            'career_year', 
            'profile_data', 
            'tech_stacks', 
            'careers', 
            'academic_records', 
            'certificates', 
            'languages'
        ]

class SimpleProfileSerializer(serializers.ModelSerializer):
    pdf_data = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['profile_id', 'name', 'job_category', 'career_year', 'pdf_data']

    def get_pdf_data(self, obj):
        # ProfileData가 존재할 경우 pdf_data를 반환
        if hasattr(obj, 'profile_data'):
            return obj.profile_data.pdf_data.url if obj.profile_data.pdf_data else None
        return None