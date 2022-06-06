from rest_framework.permissions import BasePermission
from apps.account.models import CustomUser


class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.user_type == CustomUser.CLIENT:
                return True