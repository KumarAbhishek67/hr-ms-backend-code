# from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HR, Candidate
from .serializers import HRSignupSerializer, CandidateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import TechArea, Qualification, CandidateTechArea, DomainInterest
from .serializers import TechAreaSerializer, QualificationSerializer, CandidateTechAreaSerializer, DomainInterestSerializer
from .permission import AllowRefreshTokenOnly  # Import custom permission

# Create your views here.

# this is my signup API

class HRSignupView(APIView):
    def post(self, request):
        serializer = HRSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "HR registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# this is my login API
class HRLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

class HRLoginView(TokenObtainPairView):
    serializer_class = HRLoginSerializer
    
# this is my Logout API
class HRLogoutView(APIView):
    permission_classes = [AllowRefreshTokenOnly]  # ✅ Sirf refresh token check hoga

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# this is my Candidate API
class AddCandidateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        candidates = Candidate.objects.filter(is_deleted=False)
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Candidate added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CandidateRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Candidate.objects.get(pk=pk, is_deleted=False)
        except Candidate.DoesNotExist:
            return None

    def get(self, request, pk):
        candidate = self.get_object(pk)
        if candidate:
            serializer = CandidateSerializer(candidate)
            return Response(serializer.data)
        return Response({"detail": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        candidate = self.get_object(pk)
        if candidate:
            serializer = CandidateSerializer(candidate, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        candidate = self.get_object(pk)
        if candidate:
            candidate.is_deleted = True
            candidate.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

# class TechAreaViewSet(APIView):
#     queryset = TechArea.objects.all()
#     serializer_class = TechAreaSerializer

# class QualificationViewSet(APIView):
#     queryset = Qualification.objects.all()
#     serializer_class = QualificationSerializer

# class CandidateTechAreaViewSet(APIView):
#     queryset = CandidateTechArea.objects.all()
#     serializer_class = CandidateTechAreaSerializer        

# TechArea API
class TechAreaListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tech_areas = TechArea.objects.filter(is_deleted=False)
        serializer = TechAreaSerializer(tech_areas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TechAreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "TechArea created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TechAreaRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return TechArea.objects.get(pk=pk, is_deleted=False)
        except TechArea.DoesNotExist:
            return None

    def get(self, request, pk):
        tech_area = self.get_object(pk)
        if tech_area:
            serializer = TechAreaSerializer(tech_area)
            return Response(serializer.data)
        return Response({"detail": "TechArea not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        tech_area = self.get_object(pk)
        if tech_area:
            serializer = TechAreaSerializer(tech_area, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "TechArea updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "TechArea not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        tech_area = self.get_object(pk)
        if tech_area:
            tech_area.is_deleted = True
            tech_area.save()
            return Response({"message": "TechArea deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "TechArea not found"}, status=status.HTTP_404_NOT_FOUND)

# Qualification API
class QualificationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qualifications = Qualification.objects.filter(is_deleted=False)
        serializer = QualificationSerializer(qualifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QualificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Qualification created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QualificationRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Qualification.objects.get(pk=pk, is_deleted=False)
        except Qualification.DoesNotExist:
            return None

    def get(self, request, pk):
        qualification = self.get_object(pk)
        if qualification:
            serializer = QualificationSerializer(qualification)
            return Response(serializer.data)
        return Response({"detail": "Qualification not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        qualification = self.get_object(pk)
        if qualification:
            serializer = QualificationSerializer(qualification, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Qualification updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Qualification not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        qualification = self.get_object(pk)
        if qualification:
            qualification.is_deleted = True
            qualification.save()
            return Response({"message": "Qualification deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Qualification not found"}, status=status.HTTP_404_NOT_FOUND)

# CandidateTechArea API
class CandidateTechAreaListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        candidate_tech_areas = CandidateTechArea.objects.filter(is_deleted=False)
        serializer = CandidateTechAreaSerializer(candidate_tech_areas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CandidateTechAreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "CandidateTechArea created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CandidateTechAreaRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CandidateTechArea.objects.get(pk=pk, is_deleted=False)
        except CandidateTechArea.DoesNotExist:
            return None

    def get(self, request, pk):
        candidate_tech_area = self.get_object(pk)
        if candidate_tech_area:
            serializer = CandidateTechAreaSerializer(candidate_tech_area)
            return Response(serializer.data)
        return Response({"detail": "CandidateTechArea not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        candidate_tech_area = self.get_object(pk)
        if candidate_tech_area:
            serializer = CandidateTechAreaSerializer(candidate_tech_area, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "CandidateTechArea updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "CandidateTechArea not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        candidate_tech_area = self.get_object(pk)
        if candidate_tech_area:
            candidate_tech_area.is_deleted = True
            candidate_tech_area.save()
            return Response({"message": "CandidateTechArea deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "CandidateTechArea not found"}, status=status.HTTP_404_NOT_FOUND)
    
# DomainInterest API
class DomainInterestListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        domain_interests = DomainInterest.objects.filter(is_deleted=False)
        serializer = DomainInterestSerializer(domain_interests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DomainInterestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "DomainInterest created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    serializer_class = DomainInterestSerializer

    def get_queryset(self):
        """
        Fetch active records by default. If `include_deleted=true`, fetch all records.
        """
        include_deleted = self.request.query_params.get('include_deleted', 'false')
        if include_deleted.lower() == 'true':
            return DomainInterest.objects.all()  # ✅ Fetch all (active + deleted)
        return DomainInterest.objects.filter(is_deleted=False)  # ✅ Fetch only active
    
class RestoreDomainInterestView(APIView):
    """API to Restore Deleted Domain Interest"""
    def post(self, request, pk):
        try:
            domain_interest = DomainInterest.objects.get(pk=pk, is_deleted=True)
            domain_interest.restore()
            return Response({"message": "Domain Interest restored successfully"}, status=status.HTTP_200_OK)
        except DomainInterest.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        
class DomainInterestRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return DomainInterest.objects.get(pk=pk, is_deleted=False)
        except DomainInterest.DoesNotExist:
            return None    
        
    
    def put(self, request, pk):
        domain_interest = self.get_object(pk)
        if domain_interest:
            serializer = DomainInterestSerializer(domain_interest, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Domain Interest updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Domain Interest not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        domain_interest = self.get_object(pk)
        if domain_interest:
            domain_interest.is_deleted = True
            domain_interest.save()
            return Response({"message": "Domain Interest deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Domain Interest not found"}, status=status.HTTP_404_NOT_FOUND)    