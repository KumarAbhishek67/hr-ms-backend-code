from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", HRSignupView.as_view(), name="hr-signup"),
    path("login/", HRLoginView.as_view(), name="hr-login"),
    path("logout/", HRLogoutView.as_view(), name="hr-logout"),
    path('add-candidate/', AddCandidateView.as_view(), name='add-candidate'),
    path('domain-interest/', DomainInterestView.as_view(), name='domain-interest'),
    path('tech-area/', TechAreaView.as_view(), name='tech-area'),
    path('qualification/', QualificationView.as_view(), name='qualification'),
    path('candidate-tech-area/', CandidateTechAreaView.as_view(), name='candidate-tech-area'),

    ]
