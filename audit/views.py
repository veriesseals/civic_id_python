from django.shortcuts import render
from rest_framework import viewsets
from .models import AuditLog
from .models import AuditLogSerializer

# Create your views here.
# ---------------------------------------------------------------

# Using ModelViewSet to automatically provide list, create, retrieve, update, and destroy actions.
# This allows us to easily manage our AuditLog objects through the API without having to write additional code for each action.
# ---------------------------------------------------------------
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    # The queryset defines the set of data that will be used for the viewset. In this case, we are retrieving all AuditLog objects from the database.
    # ---------------------------------------------------------------
    queryset = AuditLog.objects.all()
    # The serializer_class specifies the serializer that will be used to convert the AuditLog objects to and from JSON format. This allows us to easily serialize and deserialize our data when interacting with the API.
    # ---------------------------------------------------------------
    serializer_class = AuditLogSerializer

