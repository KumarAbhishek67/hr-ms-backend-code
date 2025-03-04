# from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class HRSignupView(APIView):
    def post(self, request):
        serializer = HRsignupserializer(data=request.data)
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
        
class AddCandidateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Candidateserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Candidate added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BaseCRUDView(APIView):
    permission_classes = [IsAuthenticated]
    model = None
    serializer_class = None
    
    def get(self, request, pk=None):
        if pk:
            obj = get_object_or_404(self.model, pk=pk, is_deleted=False)
            serializer = self.serializer_class(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        objects = self.model.objects.filter(is_deleted=False)
        serializer = self.serializer_class(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk, is_deleted=False)
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk, is_deleted=False)
        obj.is_deleted = True
        obj.save()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def restore(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk, is_deleted=True)
        obj.is_deleted = False
        obj.save()
        return Response({"message": "Restored successfully"}, status=status.HTTP_200_OK)
    
class DomainInterestView(BaseCRUDView):
    model = DomainInterest
    serializer_class = DomainInterestserializer

class TechAreaView(BaseCRUDView):
    model = TechArea
    serializer_class = TechAreaserializer

class QualificationView(BaseCRUDView):
    model = Qualification
    serializer_class = Qualificationserializer

class CandidateTechAreaView(BaseCRUDView):
    model = CandidateTechArea
    serializer_class = CandidateTechAreaserializer
