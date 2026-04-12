from rest_framework.permissions import BasePermission


# Custom permission that only allows users with
# the LAW_ENFORCEMENT role to access this endpoint
# ----------------------------------------------

class IsLawEnforcement(BasePermission):
    
    # This message is returned when access is denied
    # ----------------------------------------------
    message = "Access restricted to Law Enforcement personnel only."
    
    def has_permission(self, request, view):
        
        # User must be authenticated AND have the
        # LAW_ENFORCEMENT role — both conditions required
        # ----------------------------------------------
        
        return (
            # Check if the user is authenticated
            # ----------------------------------------------
            request.user.is_authenticated and
            request.user.role == "LAW_ENFORCEMENT"
        )