from rest_framework import serializers
from HRMSAPP.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class HRserializer(serializers.ModelSerializer):
    class Meta:
        model = HR
        fields = '__all__'
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True, 'write_only': True},
            'first_name':{'required':True},
            'last_name':{'required':True},
        }

    def create(self, validated_data):
            user = HR.objects.create(
                email=validated_data['email'],
                username=validated_data['username'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                date_of_birth=validated_data.get('date_of_birth'),
                contact_number=validated_data.get('contact_number'),
                gender=validated_data.get('gender'),
                address=validated_data.get('address'),
            )
            user.set_password(validated_data['password']) 
            user.save()
            return user
    

class HRLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token