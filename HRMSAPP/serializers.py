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
    

# Domain Interest Serializer
class DomainInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainInterest
        fields = '__all__'
        extra_kwargs = {'domain_name': {'required': True}}

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['modified_by'] = request.user
            validated_data['modified_date'] = timezone.now()
        return DomainInterest.objects.create(**validated_data)

# Qualification Serializer
class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'
        extra_kwargs = {
            'qualification_name': {'required': True},
            'qualification_desc': {'required': True},
        }

# Tech Area Serializer
class TechAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechArea
        fields = '__all__'
        extra_kwargs = {'tech_specification': {'required': True}}

# Candidate Tech Area Serializer
class CandidateTechAreaSerializer(serializers.ModelSerializer):
    candidate = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all())
    tech_area = serializers.PrimaryKeyRelatedField(queryset=TechArea.objects.all())

    class Meta:
        model = CandidateTechArea
        fields = ['tech_area','candidate']
        depth = 1
        extra_kwargs = {
            'tech_area': {'required': True},
            'candidate': {'required': True},
        }

# Candidate Serializer
# class CandidateSerializer(serializers.ModelSerializer):
#     domain_of_interest = DomainInterestSerializer(read_only=True)  
#     highest_Qualification = QualificationSerializer(read_only=True)
#     # domain_of_interest = DomainInterestSerializer()
#     # highest_Qualification = QualificationSerializer()  
#     tech_areas = CandidateTechAreaSerializer(source='candidate_tech_areas', many=True, read_only=True)

#     # domain_of_interest_id = serializers.PrimaryKeyRelatedField(
#     #     queryset=DomainInterest.objects.all(), source='domain_of_interest', write_only=True
#     # )
#     # highest_Qualification_id = serializers.PrimaryKeyRelatedField(
#     #     queryset=Qualification.objects.all(), source='highest_Qualification', write_only=True
#     # )
#     domain_of_interest = serializers.PrimaryKeyRelatedField(
#         queryset=DomainInterest.objects.all(), write_only=True
#     )
#     highest_Qualification = serializers.PrimaryKeyRelatedField(
#         queryset=Qualification.objects.all(), write_only=True
#     )

#     domain_of_interest_detail = DomainInterestSerializer(source='domain_of_interest', read_only=True)
#     highest_Qualification_detail = QualificationSerializer(source='highest_Qualification', read_only=True) 
#     class Meta:
#         model = Candidate
#         fields = '__all__'
#         extra_kwargs = {
#             'name': {'required': True},
#             'email': {'required': True},
#             'mobile': {'required': True},
#             'date_of_birth': {'required': True},
#             'resume': {'required': True},
#             'father_name': {'required': True},
#             'address': {'required': True},
#             'state': {'required': True},
#             'city': {'required': True},
#             'any_gap': {'required': True},
#         }

class CandidateSerializer(serializers.ModelSerializer):
    domain_of_interest_detail = DomainInterestSerializer(source='domain_of_interest', read_only=True)
    highest_Qualification_detail = QualificationSerializer(source='highest_Qualification', read_only=True)

   
    tech_areas = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'mobile': {'required': True},
            'date_of_birth': {'required': True},
            'resume': {'required': True},
            'father_name': {'required': True},
            'address': {'required': True},
            'state': {'required': True},
            'city': {'required': True},
            'any_gap': {'required': True},
        }

    def get_tech_areas(self, obj):
        """CandidateTechArea me se unique TechArea fetch karega"""
        tech_areas = TechArea.objects.filter(candidatetecharea__candidate=obj).distinct()
        return TechAreaSerializer(tech_areas, many=True).data

# Interview Serializer
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