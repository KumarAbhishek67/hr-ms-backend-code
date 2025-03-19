from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    HRSignupView, HRLoginView, HRLogoutView, AddCandidateView, CandidateRetrieveUpdateDeleteView,
    TechAreaListCreateView, TechAreaRetrieveUpdateDeleteView,
    QualificationListCreateView, QualificationRetrieveUpdateDeleteView,
    CandidateTechAreaListCreateView, CandidateTechAreaRetrieveUpdateDeleteView,
    DomainInterestListCreateView, DomainInterestRetrieveUpdateDeleteView,
    InterviewListCreateView, InterviewRetrieveUpdateDeleteView, RescheduleInterviewView,
    CandidateSearchView, QualificationSearchView,
    CandidateSearchView, QualificationSearchView
)

urlpatterns = [
    path("signup/", HRSignupView.as_view(), name="hr-signup"),
    path("login/", HRLoginView.as_view(), name="hr-login"),
    path("logout/", HRLogoutView.as_view(), name="hr-logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    path("add-candidate/", AddCandidateView.as_view(), name="add-candidate"),
    path("candidates-delete-update/<int:pk>/", CandidateRetrieveUpdateDeleteView.as_view(), name="candidate-retrieve-update-delete"),

    path("tech-areas/", TechAreaListCreateView.as_view(), name="tech-area-list-create"),
    path("tech-areas/<int:pk>/", TechAreaRetrieveUpdateDeleteView.as_view(), name="tech-area-retrieve-update-delete"),

    path("qualifications/", QualificationListCreateView.as_view(), name="qualification-list-create"),
    path("qualifications/<int:pk>/", QualificationRetrieveUpdateDeleteView.as_view(), name="qualification-retrieve-update-delete"),

    path("candidate-tech-areas/", CandidateTechAreaListCreateView.as_view(), name="candidate-tech-area-list-create"),
    path("candidate-tech-areas/<int:pk>/", CandidateTechAreaRetrieveUpdateDeleteView.as_view(), name="candidate-tech-area-retrieve-update-delete"),

    path("domain-interests/", DomainInterestListCreateView.as_view(), name="domain-interest-list-create"),
    path("domain-interests/<int:pk>/", DomainInterestRetrieveUpdateDeleteView.as_view(), name="domain-interest-retrieve-update-delete"),

    path("interviews/", InterviewListCreateView.as_view(), name="interview-list-create"),
    path("interviews/<int:pk>/", InterviewRetrieveUpdateDeleteView.as_view(), name="interview-retrieve-update-delete"),
    path("interviews/reschedule/<int:pk>/", RescheduleInterviewView.as_view(), name="interview-reschedule"),

    path("candidates/search/", CandidateSearchView.as_view(), name="candidate-search"),
    path("qualifications/search/", QualificationSearchView.as_view(), name="qualification-search"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
