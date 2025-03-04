# from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.utils import timezone

from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class HRSignupView(APIView):
    def post(self, request):
        serializer = HRserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "HR registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HRLoginView(TokenObtainPairView):
    serializer_class = HRLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        request.session['user_id'] = user.id  # Store session
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class HRLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            if 'user_id' in request.session:
                del request.session['user_id']  # Delete session
                return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No active session'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)