from django.shortcuts import render
from rest_framework import viewsets
from .models import ImmigrationStatus
from .serializers import ImmigrationStatusSerializer

# Create your views here.
# -----------------------------------------------------------------------------

# ImmigrationStatusViewSet provides list, create, retrieve,
# update, and destroy actions automatically via ModelViewSet
# --------------------------------------------

class ImmigrationStatusViewSet(viewsets.ModelViewSet):
    # Retrieve all ImmigrationStatus records from the database
    # --------------------------------------------
    queryset = ImmigrationStatus.objects.all()
    # Use ImmigrationStatusSerializer to convert records to/from JSON
    # --------------------------------------------
    serializer_class = ImmigrationStatusSerializer

