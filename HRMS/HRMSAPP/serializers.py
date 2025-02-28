from rest_framework import serializers
from .models import HR, Candidate  # ✅ Ensure 'Candidate' Model is Imported

class HRSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HR
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = HR(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # ✅ Password Hashing
        user.save()
        return user

# ✅ Candidate Serializer
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'  # ✅ Ensure all fields are serialized
