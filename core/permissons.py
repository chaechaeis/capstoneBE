from rest_framework.permissions import BasePermission


class IsSetter(BasePermission):
    """
    Allows access only authenticate and "Setter" users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "setter"
        )


class IsSeeker(BasePermission):
    """
    Allows access only authenticate and "Seeker" users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "seeker"
        )
