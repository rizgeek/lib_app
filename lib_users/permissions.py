from rest_framework.permissions import BasePermission

class IsInGroup(BasePermission):
    def __init__(self, *group_names):
        self.group_names = group_names

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        user_groups = [group.name for group in user.groups.all()]
        return any(group_name in user_groups for group_name in self.group_names)
