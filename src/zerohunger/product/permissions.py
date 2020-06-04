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


class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner to perform this operation'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.farmer_id.email == request.user.email
