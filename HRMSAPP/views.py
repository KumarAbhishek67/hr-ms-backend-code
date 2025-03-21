# from django.shortcuts import render
from rest_framework import status
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HR, Candidate
from django.utils.timezone import now
from .serializers import HRSignupSerializer, CandidateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import TechArea, Qualification, CandidateTechArea, DomainInterest
from .models import Interview
from .serializers import TechAreaSerializer, QualificationSerializer, CandidateTechAreaSerializer, DomainInterestSerializer, InterviewSerializer
from .permission import AllowRefreshTokenOnly  # Import custom permission
from django.db import models
from django.db.models import Q

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
    permission_classes = [AllowRefreshTokenOnly]

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

# Candidate Search View API
class CandidateSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Query parameter `q` is required"}, status=status.HTTP_400_BAD_REQUEST)

        candidates = Candidate.objects.filter(is_deleted=False).filter(
            Q(name__icontains=query) | Q(mobile__icontains=query) 
        )

        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# this is my Candidate API
class AddCandidateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        candidates = Candidate.objects.filter(is_deleted=False).prefetch_related('candidate_tech_areas__tech_area').all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        tech_areas_data = request.data.pop('tech_areas', [])  #Tech areas ka data extract kiya
        serializer = CandidateSerializer(data=request.data)

        if serializer.is_valid():
            candidate = serializer.save()  #Pehle Candidate ka record save karo
            
            # Tech Areas ko CandidateTechArea table me insert karo
            for tech_area_id in tech_areas_data:
                tech_area = TechArea.objects.get(id=tech_area_id)
                CandidateTechArea.objects.create(candidate=candidate, tech_area=tech_area)
            
            return Response({"message": "Candidate added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
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
        return Response({"detail": "Candidate not found Please enter a vlaid id"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        candidate = self.get_object(pk)
        if candidate:
            tech_areas_data = request.data.pop('tech_areas', [])  # Tech areas extract kiya
            serializer = CandidateSerializer(candidate, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                # Pehle existing tech_areas delete karo
                CandidateTechArea.objects.filter(candidate=candidate).delete()

                # Naye tech_areas insert karo
                for tech_area_id in tech_areas_data:
                    tech_area = TechArea.objects.get(id=tech_area_id)
                    CandidateTechArea.objects.create(candidate=candidate, tech_area=tech_area)

                return Response({"message": "Candidate updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        candidate = self.get_object(pk)
        if candidate:
            candidate.is_deleted = True
            candidate.save()
            return Response({"message": "Candidate deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

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

# Qualification search API
class QualificationSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qualification_name = request.query_params.get('qualification', '')
        if not qualification_name:
            return Response({"error": "Qualification parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        qualification = Qualification.objects.filter(qualification_name__iexact=qualification_name).first()

        if not qualification:
            return Response({"error": "No candidates found for this qualification"}, status=status.HTTP_404_NOT_FOUND)

        serializer = QualificationSerializer(qualification)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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

class CandidateTechAreaListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        candidate_tech_areas = CandidateTechArea.objects.filter(is_deleted=False).select_related('candidate').prefetch_related('tech_area')
        serializer = CandidateTechAreaSerializer(candidate_tech_areas, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        
        try:
            candidate = Candidate.objects.get(id=data.get('candidate'))
            tech_area = TechArea.objects.get(id=data.get('tech_area'))
        except Candidate.DoesNotExist:
            return Response({"error": "Invalid Candidate ID"}, status=status.HTTP_400_BAD_REQUEST)
        except TechArea.DoesNotExist:
            return Response({"error": "Invalid TechArea ID"}, status=status.HTTP_400_BAD_REQUEST)

        # data['candidate'] = candidate.id
        # data['tech_area'] = tech_area.id

        serializer = CandidateTechAreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "CandidateTechArea created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateTechAreaRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return CandidateTechArea.objects.filter(pk=pk, is_deleted=False).first()

    def get(self, request, pk):
        candidate_tech_area = self.get_object(pk)
        if candidate_tech_area:
            serializer = CandidateTechAreaSerializer(candidate_tech_area)
            return Response(serializer.data)
        return Response({"detail": "CandidateTechArea not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        candidate_tech_area = self.get_object(pk)
        if not candidate_tech_area:
            return Response({"detail": "CandidateTechArea not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()

        if 'candidate' in data:
            try:
                candidate = Candidate.objects.get(id=data.get('candidate'))
                data['candidate'] = candidate.id
            except Candidate.DoesNotExist:
                return Response({"error": "Invalid Candidate ID"}, status=status.HTTP_400_BAD_REQUEST)

        if 'tech_area' in data:
            try:
                tech_area = TechArea.objects.get(id=data.get('tech_area'))
                data['tech_area'] = tech_area.id
            except TechArea.DoesNotExist:
                return Response({"error": "Invalid TechArea ID"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CandidateTechAreaSerializer(candidate_tech_area, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "CandidateTechArea updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        candidate_tech_area = self.get_object(pk)
        if candidate_tech_area:
            candidate_tech_area.is_deleted = True
            candidate_tech_area.save()
            return Response({"message": "CandidateTechArea deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "CandidateTechArea not found"}, status=status.HTTP_404_NOT_FOUND)

        
class DomainInterestListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ Fetch all active domain interests """
        domain_areas = DomainInterest.objects.filter(is_deleted=False)
        serializer = DomainInterestSerializer(domain_areas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ Add new domain interest or restore deleted one """
        domain_name = request.data.get('domain_name')

        # 1. Check if deleted entry exists
        existing_domain = DomainInterest.objects.filter(domain_name=domain_name).first()

        if existing_domain:
            if existing_domain.is_deleted:
                existing_domain.is_deleted = False
                existing_domain.deleted_date = None  
                existing_domain.deleted_by = None  
                existing_domain.modified_by = request.user  
                existing_domain.modified_date = timezone.now()  
                existing_domain.save()
                return Response({"message": "Domain interest restored successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Domain interest already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Create new domain interest
        serializer = DomainInterestSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()  # Don't pass extra fields here, they are handled in `create()` method
            return Response({"message": "Domain interest created successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DomainInterestRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return DomainInterest.objects.get(id=pk, is_deleted=False)
        except DomainInterest.DoesNotExist:
            return None

    def get(self, request, pk):
        domain = self.get_object(pk)
        if domain:
            serializer = DomainInterestSerializer(domain)
            return Response(serializer.data)
        return Response({"error": "Domain interest not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        domain = self.get_object(pk)
        if domain:
            serializer = DomainInterestSerializer(domain, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Domain interest not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        domain = self.get_object(pk)
        if domain:
            domain.is_deleted = True
            domain.deleted_by = request.user
            domain.deleted_date = timezone.now()
            domain.save()
            return Response({"message": "Domain interest deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Domain interest not found"}, status=status.HTTP_404_NOT_FOUND)   

# Interview API
class InterviewListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            interviews = Interview.objects.filter(is_deleted=False)
            serializer = InterviewSerializer(interviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = InterviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InterviewRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Interview.objects.get(id=pk, is_deleted=False)
        except Interview.DoesNotExist:
            return None

    def get(self, request, pk):
        interview = self.get_object(pk)
        if interview is None:
            return Response({"error": "Interview not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = InterviewSerializer(interview)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        interview = self.get_object(pk)
        if interview is None:
            return Response({"error": "Interview not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            serializer = InterviewSerializer(interview, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        interview = self.get_object(pk)
        if interview is None:
            return Response({"error": "Interview not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            interview.is_deleted = True
            interview.DeletedByUserid = request.user
            interview.DeletedDateTime = now()
            interview.save()
            return Response({"message": "Interview marked as deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RescheduleInterviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            interview = Interview.objects.get(id=pk, is_deleted=False)
            
            new_date = request.data.get("rescheduled_date")
            new_time = request.data.get("rescheduled_time")
            
            if not new_date or not new_time:
                return Response({"error": "Rescheduled date and time are required."}, status=status.HTTP_400_BAD_REQUEST)
            
            interview.interview_date = new_date
            interview.interview_time = new_time
            interview.ModifiedByUserid = request.user
            interview.ModifyDateTime = now()
            interview.save()
            
            return Response({"message": "Interview successfully rescheduled!", "new_date": new_date, "new_time": new_time}, status=status.HTTP_200_OK)
        
        except Interview.DoesNotExist:
            return Response({"error": "Interview not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)