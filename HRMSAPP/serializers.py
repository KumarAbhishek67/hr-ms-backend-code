from rest_framework import serializers
from .models import HR, Candidate ,TechArea, Qualification, CandidateTechArea, DomainInterest # ✅ Ensure 'Candidate' Model is Imported

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
            'date_of_birth': {'required': True}
        }

class TechAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechArea
        fields = '__all__'
        extra_kwargs = {
            'tech_specification': {'required': True},
        }

class QualificationSerializer(serializers.ModelSerializer):
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
        fields = '__all__'        
        extra_kwargs = {
            'domain_name': {'required': True},
        }
