from django.urls import path
from .views import HRSignupView, HRLoginView, HRLogoutView, AddCandidateView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import  CandidateRetrieveUpdateDeleteView
from .views import TechAreaListCreateView, TechAreaRetrieveUpdateDeleteView
from .views import QualificationListCreateView, QualificationRetrieveUpdateDeleteView
from .views import CandidateTechAreaListCreateView, CandidateTechAreaRetrieveUpdateDeleteView, DomainInterestListCreateView, DomainInterestRetrieveUpdateDeleteView, RestoreDomainInterestView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("signup/", HRSignupView.as_view(), name="hr-signup"),
    path("login/", HRLoginView.as_view(), name="hr-login"),
    path("logout/", HRLogoutView.as_view(), name="hr-logout"),
    path("add-candidate/", AddCandidateView.as_view(), name="add-candidate"),
    path("candidates/<int:pk>/", CandidateRetrieveUpdateDeleteView.as_view(), name="candidate-retrieve-update-delete"),

    # TechArea-related URLs
    path("tech-areas/", TechAreaListCreateView.as_view(), name="tech-area-list-create"),
    path("tech-areas/<int:pk>/", TechAreaRetrieveUpdateDeleteView.as_view(), name="tech-area-retrieve-update-delete"),

    # Qualification-related URLs
    path("qualifications/", QualificationListCreateView.as_view(), name="qualification-list-create"),
    path("qualifications/<int:pk>/", QualificationRetrieveUpdateDeleteView.as_view(), name="qualification-retrieve-update-delete"),

    # CandidateTechArea-related URLs
    path("candidate-tech-areas/", CandidateTechAreaListCreateView.as_view(), name="candidate-tech-area-list-create"),
    path("candidate-tech-areas/<int:pk>/", CandidateTechAreaRetrieveUpdateDeleteView.as_view(), name="candidate-tech-area-retrieve-update-delete"),
    
    #domain interest
    path("domain-interests/", DomainInterestListCreateView.as_view(), name="domain-interest-list-create"),
    path("domain-interest/<int:pk>/", DomainInterestRetrieveUpdateDeleteView.as_view(), name="domain-interest-retrieve-update-delete"),
    path('domain-interest/restore/<int:pk>/', RestoreDomainInterestView.as_view(), name='domain-interest-restore'),

    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
# ✅ Media files ko serve karne ke liye
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)