from rest_framework.permissions import BasePermission


class IsLawEnforcement(BasePermission):
    message = "Access restricted to Law Enforcement personnel only."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # True Django superusers should always be allowed
        if getattr(user, "is_superuser", False):
            return True

        # Fallback to your custom role field
        return getattr(user, "role", None) in ("LAW_ENFORCEMENT", "SUPER_ADMIN")