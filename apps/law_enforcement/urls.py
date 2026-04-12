from django.urls import path
from .views import VerificationRequestView, VerificationHistoryView


# Law Enforcement API URL patterns
# ----------------------------------------------

urlpatterns = [
    # POST to this endpoint to perform a lookup
    # requires: person id + reason
    # ----------------------------------------------
    path(
        "verify/",
        VerificationRequestView.as_view(),
        name="le-verify"
    ),
    # GET to this endpoint to view lookup history
    # ----------------------------------------------
    path(
        "history/",
        VerificationHistoryView.as_view(),
        name="le-history"
    )
]