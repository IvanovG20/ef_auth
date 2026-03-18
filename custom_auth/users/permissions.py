from rest_framework.permissions import BasePermission
from .models import UserPermission


class HasPermission(BasePermission):

    def __init__(self, resource, action):
        self.resource = resource
        self.action = action

    def has_permission(self, request, view):
        user = request.user

        if not user:
            return False

        return UserPermission.objects.filter(
            user=user,
            resource=self.resource,
            action=self.action
        ).exists()
