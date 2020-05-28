from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsFarmerOrReadOnly(BasePermission):
    message = 'Only a Farmer can perform this operation'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if user.isFarmer:
            return True
        return False
