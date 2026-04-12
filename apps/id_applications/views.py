from django.shortcuts import render
from rest_framework import viewsets
from .models import IDApplication
from .serializers import IDApplicationSerializer

# Create your views here.
# ---------------------------------------------------------------

# Using ModelViewSet to automatically provide list, create, retrieve, update, and destroy actions.
# This allows us to easily manage our IDApplication objects through the API without having to write additional code for each action.
# ---------------------------------------------------------------
class IDApplicationViewSet(viewsets.ModelViewSet):
    # The queryset defines the set of data that will be used for the viewset. In this case, we are retrieving all IDApplication objects from the database.
    # ---------------------------------------------------------------
    queryset = IDApplication.objects.all()
    # The serializer_class specifies the serializers that will be used to convert the IDApplication objects to and from JSON format. This allows us to easily serialize and deserialize our data when interacting with the API.
    # ---------------------------------------------------------------
    serializer_class = IDApplicationSerializer