from django.urls import path
from .views import HRSignupView, HRLoginView, HRLogoutView, AddCandidateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", HRSignupView.as_view(), name="hr-signup"),
    path("login/", HRLoginView.as_view(), name="hr-login"),
    path("logout/", HRLogoutView.as_view(), name="hr-logout"),
    path("add-candidate/", AddCandidateView.as_view(), name="add-candidate"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
