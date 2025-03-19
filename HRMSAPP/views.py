from django.contrib.auth import authenticate, login
# from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.contrib.sessions.backends.db import SessionStore
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from django.utils import timezone
from django.db.models import Q  # 👈 Yeh line add karni hai

# from django.shortcuts import get_object_or_404
# from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class HRSignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = HRsignupserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "HR registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HRLoginView(APIView):
    permission_classes = [AllowAny]
#This is using JWT refresh token login but will be needed to add tokenobtainpairview() & tokenrefreshview()


    # def post(self, request):
    #     email = request.data.get("email")
    #     password = request.data.get("password")

    #     user = authenticate(request, username=email, password=password)  # Assuming email as username
    #     if user is not None:
    #         refresh = RefreshToken.for_user(user)  # Generate JWT tokens
            
    #         return Response({
    #             'access_token': str(refresh.access_token),
    #             'refresh_token': str(refresh)
    #         }, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


#This login using Session and token same as BDE


    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = HR.objects.get(email=email)
        except HR.DoesNotExist:
            return Response({"response": "No User exists"}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, user.password):
            return Response({"response": "Incorrect Password"}, status=status.HTTP_401_UNAUTHORIZED)

        if user.is_deleted:
            return Response({'response': 'No User Found'}, status=status.HTTP_204_NO_CONTENT)

        # datejoined=timezone.datetime.today().date()
        

        session = SessionStore()
        session['user_id'] = user.id
        session['user_email'] = email
        session.save()

        session_key = session.session_key

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'session_key': session_key,
            'email': user.email ,
            'first_name': user.first_name,
            'last_name': user.last_name
        }, status=status.HTTP_200_OK)     


    #using CSRF


#     def post(self, request):
#         email = request.data.get("email")
#         password = request.data.get("password")

#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             login(request, user)  # Logs the user in and creates a session
            
#             # Store additional user details in session
#             request.session['user_info'] = {
#                 'user_id': user.id,
#                 'email': user.email,
#                 'last_login': str(timezone.now())  # Store last login timestamp
#             }
          
#             return Response({
#                 'message': 'Login successful',
#                 'user_info': request.session['user_info']
#             }, status=status.HTTP_200_OK)

#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class HRLogoutView(APIView):

    #this logout using jwt refresh token but will be needed to add tokenobtainpairview() & tokenrefreshview()

    # permission_classes = [AllowAny]  # Anyone can access logout

    # def post(self, request):
    #     try:
    #         refresh_token = request.data.get('refresh_token')
    #         if refresh_token:
    #             token = RefreshToken(refresh_token)
    #             token.blacklist()  # Blacklist the refresh token
    #             return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({'error': 'Refresh token missing'}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)



    #This logout using session+token same as BDE


    # permission_classes = [IsAuthenticated]
    def post(self, request):
        session_key = request.data.get('session_key')
        # session_key = SessionStore(session_key=session_key)
      
        if session_key:
            try:
                session = SessionStore(session_key=session_key)
                user_id = session.get('user_id')
               
                if user_id:
                    try:
                      
                        user_data=HR.objects.get(id=user_id)
                        user_data.last_login = timezone.now()
                        user_data.save()  

                        session.delete()

                        return Response({'response': 'User Logout Successfully'}, status=status.HTTP_200_OK)
                    except HR.DoesNotExist:
                        pass
            except Exception as e:
                pass
        return Response({'response': 'You are not logged in!'}, status=status.HTTP_204_NO_CONTENT)
    

    #using CSRF sessions


    # def post(self, request):
    #     try:
    #         if 'user_info' in request.session:
    #             del request.session['user_info']  # Remove user session data
    #             return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({'error': 'No active session'}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'error': 'Logout failed'}, status=status.HTTP_400_BAD_REQUEST)

class CandidateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        candidates = Candidate.objects.filter(is_deleted=False)
        serializer = Candidateserializer(candidates, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        existing_candidate = Candidate.objects.filter(email=request.data.get('email'),is_deleted=True).first()

        if existing_candidate:
            existing_candidate.is_deleted = False
            existing_candidate.DeletedDateTime = None  
            existing_candidate.ModifiedByUserid = request.user
            existing_candidate.ModifyDateTime = timezone.now()
            existing_candidate.save()
            return Response({"message": "Candidate restored successfully"}, status=status.HTTP_200_OK)
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
        existing_tech = TechArea.objects.filter(tech_specification=request.data.get('tech_specification'),is_deleted=True).first()

        if existing_tech:
            existing_tech.is_deleted = False
            existing_tech.DeletedDateTime = None  
            existing_tech.ModifiedByUserid = request.user
            existing_tech.ModifyDateTime = timezone.now()
            existing_tech.save()
            return Response({"message": "TechArea restored successfully"}, status=status.HTTP_200_OK)
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
        existing_domain = DomainInterest.objects.filter(domain_name=request.data.get('domain_name'),is_deleted=True).first()

        if existing_domain:
           
            existing_domain.is_deleted = False
            existing_domain.DeletedDateTime = None 
            existing_domain.ModifiedByUserid = request.user
            existing_domain.ModifyDateTime = timezone.now()
            existing_domain.save()
            return Response({"message": "Domain interest restored successfully"}, status=status.HTTP_200_OK)
        
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

        existing_qualification = Qualification.objects.filter(qualification_name=request.data.get('qualification_name'),is_deleted=True).first()

        if existing_qualification:
     
            existing_qualification.is_deleted = False
            existing_qualification.DeletedDateTime = None 
            existing_qualification.ModifiedByUserid = request.user
            existing_qualification.ModifyDateTime = timezone.now()
            existing_qualification.save()
            return Response({"message": "Qualification restored successfully"}, status=status.HTTP_200_OK)
        

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
    
class ScheduleInterviewCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        schedules = Interview.objects.filter(is_deleted=False)
        serializer = Interviewserializer(schedules, many=True)
        return Response(serializer.data)

    def post(self, request):

        existing_interview = Interview.objects.filter(candidate_profile=request.data.get('candidate_profile'),interview_date=request.data.get('interview_date'),interview_time=request.data.get('interview_time'),is_deleted=True).first()

        if existing_interview:
     
            existing_interview.is_deleted = False
            existing_interview.DeletedDateTime = None
            existing_interview.ModifiedByUserid = request.user
            existing_interview.ModifyDateTime = timezone.now()
            existing_interview.save()
            return Response({"message": "Interview restored successfully"}, status=status.HTTP_200_OK)
        

        serializer = Interviewserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ModifiedByUserid = request.user, ModifyDateTime = timezone.now())
            return Response({"message": "Interview created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InterviewUpdateDelete(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Interview.objects.get(pk=pk, is_deleted=False)
        except Interview.DoesNotExist:
            return None

    def get(self, request, pk):
        schedule = self.get_object(pk)
        if schedule:
            serializer = Interviewserializer(schedule)
            return Response(serializer.data)
        return Response({"detail": "Schedule not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        schedule = self.get_object(pk)
        if schedule:
            serializer = Interviewserializer(schedule, data=request.data)
            if serializer.is_valid():
                serializer.save(ModifiedByUserid = request.user, ModifyDateTime = timezone.now())
                return Response({"message": "Schedule updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Schedule not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        schedule = self.get_object(pk)
        if schedule:
            schedule.is_deleted = True
            schedule.DeletedByUserid=request.user
            schedule.DeletedDateTime=timezone.now()
            schedule.save()
            return Response({"message": "Schedule deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Schedule not found"}, status=status.HTTP_404_NOT_FOUND)


class SearchAPIView(APIView):
    def get(self, request):
        search_type = request.GET.get('type', '').strip()  # Remove extra spaces
        search_query = request.GET.get('query', '').strip()  # Remove extra spaces

        print(f"Search Type: {search_type}, Query: {search_query}")  # Debugging

        if search_type == "Candidate":
            candidates = Candidate.objects.filter(
                Q(name__icontains=search_query) | 
                Q(email__icontains=search_query) |
                Q(mobile__icontains=search_query)
            )

            print(f"Candidates Found: {candidates}")  # Debugging

            serializer = Candidateserializer(candidates, many=True)
            return Response(serializer.data)

        return Response({"error": "Invalid search type or no query provided."}, status=400)
