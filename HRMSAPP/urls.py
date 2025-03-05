from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", HRSignupView.as_view(), name="hr-signup"),
    path("login/", HRLoginView.as_view(), name="hr-login"),
    path("logout/", HRLogoutView.as_view(), name="hr-logout"),
    path('add-candidate/', CandidateView.as_view(), name='add-candidate'),
    path('add-candidate/<int:pk>/', CandidateGetUpdateDeleteView.as_view(), name='add-candidate'),
    path('domain-interest/', DomainInterestView.as_view(), name='domain-interest'),
    path('domain-interest/<int:pk>/', DomainInterestUpdateDeleteView.as_view(), name='domain-interest'),
    path('tech-area/', TechAreaCreateGetView.as_view(), name='tech-area'),
    path('tech-area/<int:pk>/', TechAreaUpdateDeleteView.as_view(), name='tech-area'),
    path('qualification/', QualificationCreateView.as_view(), name='qualification'),
    path('qualification/<int:pk>/', QualificationUpdateDeleteView.as_view(), name='qualification'),
    path('candidate-tech-area/', CandidateTechAreaView.as_view(), name='candidate-tech-area'),
    path('candidate-tech-area/<int:pk>/', CandidateTechAreaUpdateDeleteView.as_view(), name='candidate-tech-area'),

    ]
