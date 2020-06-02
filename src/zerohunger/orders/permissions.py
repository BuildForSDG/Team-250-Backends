from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'You must be the owner to perform this operation'

    def has_object_permission(self, request, view, obj):
        return obj.customer_id.email == request.user.email
