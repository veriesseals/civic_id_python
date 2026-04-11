from django.shortcuts import render
from rest_framework import viewsets
from .models import Person
from .serializers import PersonSerializer

# Create your views here.
# --------------------------------------------------------------


# Using ModelViewSet to automatically provide list, create, retrieve, update, and destroy actions.
# This allows us to easily manage our Person objects through the API without having to write additional code for each action.
# ---------------------------------------------------------------
class PersonViewSet(viewsets.ModelViewSet):
    # The queryset defines the set of data that will be used for the viewset. In this case, we are retrieving all Person objects from the database.
    # ---------------------------------------------------------------
    queryset = Person.objects.all()
    # The serializer_class specifies the serializer that will be used to convert the Person objects to and from JSON format. This allows us to easily serialize and deserialize our data when interacting with the API.
    # ---------------------------------------------------------------
    serializer_class = PersonSerializer 
