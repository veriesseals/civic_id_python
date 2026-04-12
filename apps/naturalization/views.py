from django.shortcuts import render
from rest_framework import viewsets
from .models import NaturalizationRecord
from .serializers import NaturalizationRecordSerializer


# Create your views here.
# ---------------------------------------------

# NaturalizationRecordViewSet provides list, create, retrieve,
# update, and destroy actions automatically via ModelViewSet
# --------------------------------------------

class NaturalizationRecordViewSet(viewsets.ModelViewSet):
    # Define the queryset to retrieve all NaturalizationRecord instances
    # --------------------------------------------
    queryset = NaturalizationRecord.objects.all()
    # Specify the serializer class to be used for converting model
    # instances to JSON and vice versa
    # --------------------------------------------
    serializer_class = NaturalizationRecordSerializer
