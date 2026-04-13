from django.urls import path
from .views import (
    EligibilityCheckView,
    RegisterVoterView,
    FlagFelonyView,
    RestoreRightsView,
)

urlpatterns = [
    path("eligibility/",  EligibilityCheckView.as_view(), name="voter-eligibility"),
    path("register/",     RegisterVoterView.as_view(),    name="voter-register"),
    path("flag-felony/",  FlagFelonyView.as_view(),       name="voter-flag-felony"),
    path("restore/",      RestoreRightsView.as_view(),    name="voter-restore"),
]