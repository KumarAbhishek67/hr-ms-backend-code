from rest_framework import serializers
from django.utils import timezone
from .models import HR, Candidate, TechArea, Qualification, CandidateTechArea, DomainInterest, Interview

class HRSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HR
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = HR(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'
        depth = 1
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'mobile': {'required': True},
            'date_of_birth': {'required': True},
            'resume': {'required': True},
        }

class TechAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechArea
        fields = '__all__'
        extra_kwargs = {
            'tech_specification': {'required': True},
        }

class QualificationSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True, source='candidate_set')  # ✅ Corrected related_name

    class Meta:
        model = Qualification
        fields = '__all__'
        extra_kwargs = {
            'qualification_name': {'required': True},
            'qualification_desc': {'required': True},
        }

class CandidateTechAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateTechArea
        fields = '__all__'
        extra_kwargs = {
            'tech_area': {'required': True},
        }

class DomainInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainInterest
        fields = '__all__'  # Ensure all model fields are included

    def create(self, validated_data):
        request = self.context.get('request', None)
        
        if request:
            validated_data['modified_by'] = request.user  # Set modified_by to request user
            validated_data['modified_date'] = timezone.now()  # Set modified_date to current time

        return DomainInterest.objects.create(**validated_data)
class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = "__all__"
        extra_kwargs = {
            'candidate_profile': {'required': True},
            'interviewers': {'required': True},
            'interview_date': {'required': True},
            'interview_time': {'required': True},
            'status': {'required': True},
        }
