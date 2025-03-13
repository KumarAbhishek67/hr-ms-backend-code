from rest_framework.permissions import BasePermission

class AllowRefreshTokenOnly(BasePermission):
    """
    Custom permission jo sirf refresh token ke liye allow karegi.
    """

    def has_permission(self, request, view):
        return "refresh" in request.data  # ✅ Agar request me refresh token hai to allow kar do