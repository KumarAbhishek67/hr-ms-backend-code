# from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class HRSignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = HRsignupserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "HR registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HRLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = HRLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        request.session['user_id'] = user.id  # Store session
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class HRLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if 'user_id' in request.session:
                del request.session['user_id']  # Delete session
                return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No active session'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        
class CandidateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        candidates = Candidate.objects.filter(is_deleted=False)
        serializer = Candidateserializer(candidates, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = Candidateserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ModifiedByUserid = request.user, ModifyDateTime = timezone.now())
            return Response({"message": "Candidate added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CandidateGetUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Candidate.objects.get(pk=pk, is_deleted=False)
        except Candidate.DoesNotExist:
            return None

    def get(self, request, pk):
        candidate = self.get_object(pk)
        if candidate:
            serializer = Candidateserializer(candidate)
            return Response(serializer.data)
        return Response({"detail": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        candidate = self.get_object(pk)
        if candidate:
            serializer = Candidateserializer(candidate, data=request.data)
            if serializer.is_valid():
                serializer.save(ModifiedByUserid = request.user, ModifyDateTime = timezone.now())
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        candidate = self.get_object(pk)
        if candidate:
            candidate.is_deleted = True
            candidate.DeletedByUserid=request.user
            candidate.DeletedDateTime=timezone.now()
            candidate.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)



class TechAreaCreateGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tech_areas = TechArea.objects.filter(is_deleted=False)
        serializer = TechAreaserializer(tech_areas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TechAreaserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ModifiedByUserid = request.user, ModifyDateTime = timezone.now())
            return Response({"message": "TechArea created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TechAreaUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return TechArea.objects.get(pk=pk, is_deleted=False)
        except TechArea.DoesNotExist:
            return None

    def get(self, request, pk):
        tech_area = self.get_object(pk)
        if tech_area:
            serializer = TechAreaserializer(tech_area)
            return Response(serializer.data)
        return Response({"detail": "TechArea not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        tech_area = self.get_object(pk)
        if tech_area:
            serializer = TechAreaserializer(tech_area, data=request.data)
            if serializer.is_valid():
                serializer.save(ModifiedByUserid = request.user, ModifyDateTime = timezone.now())
                return Response({"message": "TechArea updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "TechArea not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        tech_area = self.get_object(pk)
        if tech_area:
            tech_area.is_deleted = True
            tech_area.DeletedByUserid=request.user
            tech_area.DeletedDateTime=timezone.now()
            tech_area.save()
            return Response({"message": "TechArea deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "TechArea not found"}, status=status.HTTP_404_NOT_FOUND)

#domain interest
class DomainInterestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        domain_areas = DomainInterest.objects.filter(is_deleted=False)
        serializer = DomainInterestserializer(domain_areas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DomainInterestserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ModifiedByUserid = request.user, ModifyDateTime = timezone.now())
            return Response({"message": "Doamin Area created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DomainInterestUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return DomainInterest.objects.get(pk=pk, is_deleted=False)
        except DomainInterest.DoesNotExist:
            return None

    def get(self, request, pk):
        domain_area = self.get_object(pk)
        if domain_area:
            serializer = TechAreaserializer(domain_area)
            return Response(serializer.data)
        return Response({"detail": "Domain not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        domain_area = self.get_object(pk)
        if domain_area:
            serializer = DomainInterestserializer(domain_area, data=request.data)
            if serializer.is_valid():
                serializer.save(ModifiedByUserid = request.user, ModifyDateTime = timezone.now())
                return Response({"message": "Domain updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Domain not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        domain_area = self.get_object(pk)
        if domain_area:
            domain_area.is_deleted = True
            domain_area.DeletedByUserid=request.user
            domain_area.DeletedDateTime=timezone.now()
            domain_area.save()
            return Response({"message": "Domain deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Domain not found"}, status=status.HTTP_404_NOT_FOUND)

#end domain interest
class QualificationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qualifications = Qualification.objects.filter(is_deleted=False)
        serializer = Qualificationserializer(qualifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = Qualificationserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ModifiedByUserid = request.user, ModifyDateTime = timezone.now())
            return Response({"message": "Qualification created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QualificationUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Qualification.objects.get(pk=pk, is_deleted=False)
        except Qualification.DoesNotExist:
            return None

    def get(self, request, pk):
        qualification = self.get_object(pk)
        if qualification:
            serializer = Qualificationserializer(qualification)
            return Response(serializer.data)
        return Response({"detail": "Qualification not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        qualification = self.get_object(pk)
        if qualification:
            serializer = Qualificationserializer(qualification, data=request.data)
            if serializer.is_valid():
                serializer.save(ModifiedByUserid = request.user, ModifyDateTime = timezone.now())
                return Response({"message": "Qualification updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Qualification not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        qualification = self.get_object(pk)
        if qualification:
            qualification.is_deleted = True
            qualification.DeletedByUserid=request.user
            qualification.DeletedDateTime=timezone.now()
            qualification.save()
            return Response({"message": "Qualification deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Qualification not found"}, status=status.HTTP_404_NOT_FOUND)

class CandidateTechAreaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        candidate_tech_areas = CandidateTechArea.objects.filter(is_deleted=False)
        serializer = CandidateTechAreaserializer(candidate_tech_areas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CandidateTechAreaserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ModifiedByUserid = request.user, ModifyDateTime = timezone.now())
            return Response({"message": "CandidateTechArea created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CandidateTechAreaUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CandidateTechArea.objects.get(pk=pk, is_deleted=False)
        except CandidateTechArea.DoesNotExist:
            return None

    def get(self, request, pk):
        candidate_tech_area = self.get_object(pk)
        if candidate_tech_area:
            serializer = CandidateTechAreaserializer(candidate_tech_area)
            return Response(serializer.data)
        return Response({"detail": "CandidateTechArea not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        candidate_tech_area = self.get_object(pk)
        if candidate_tech_area:
            serializer = CandidateTechAreaserializer(candidate_tech_area, data=request.data)
            if serializer.is_valid():
                serializer.save(ModifiedByUserid = request.user, ModifyDateTime = timezone.now())
                return Response({"message": "CandidateTechArea updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "CandidateTechArea not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        candidate_tech_area = self.get_object(pk)
        if candidate_tech_area:
            candidate_tech_area.is_deleted = True
            candidate_tech_area.DeletedByUserid=request.user
            candidate_tech_area.DeletedDateTime=timezone.now()
            candidate_tech_area.save()
            return Response({"message": "CandidateTechArea deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "CandidateTechArea not found"}, status=status.HTTP_404_NOT_FOUND)