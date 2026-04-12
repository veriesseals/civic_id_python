"""
URL configuration for civicid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from immigration_status.views import ImmigrationStatusViewSet
from naturalization.views import NaturalizationRecordViewSet

# Importing the viewsets from our applications to register them with the router.
# This allows us to automatically generate the URL patterns for our API endpoints based on the viewsets we have defined in our applications.
# ---------------------------------------------------------------
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Creating a router instance to register our viewsets. The DefaultRouter will automatically generate the URL patterns for our API endpoints based on the viewsets we register with it.
# ---------------------------------------------------------------
from persons.views import PersonViewSet
from birth_records.views import BirthRecordViewSet
from audit.views import AuditLogViewSet
from id_applications.views import IDApplicationViewSet
from issued_ids.views import IssuedIDViewSet

# ----------------------------------------------
# Register all viewsets with the router
# The router automatically creates URLs for:
# GET    /api/persons/          → list all
# POST   /api/persons/          → create new
# GET    /api/persons/{id}/     → retrieve one
# PUT    /api/persons/{id}/     → update one
# DELETE /api/persons/{id}/     → delete one
# ----------------------------------------------

# Registering the viewsets with the router to generate the corresponding URL patterns for our API endpoints. This allows us to easily manage our resources through the API without having to manually define each URL pattern.
# ---------------------------------------------------------------
router = DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'birth-records', BirthRecordViewSet)
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'id-applications', IDApplicationViewSet)
router.register(r'issued-ids', IssuedIDViewSet)
router.register(r'naturalization-records', NaturalizationRecordViewSet)
router.register(r'immigration-status', ImmigrationStatusViewSet)
router.register(r'naturalization', NaturalizationRecordViewSet)




urlpatterns = [
    # Including the admin site URL pattern to allow access to the Django admin interface.
    # Including the router URLs to make our API endpoints available under the /api/ path. This allows us to access our API endpoints for managing persons, birth records, audit logs, ID applications, and issued IDs through the /api/ URL prefix.
    # ---------------------------------------------------------------
    path('admin/', admin.site.urls),
    
    # Including the JWT authentication URLs to allow users to obtain and refresh JSON Web Tokens for authentication when interacting with our API endpoints. This provides a secure way to authenticate users and manage access to our API resources.
    # ---------------------------------------------------------------
    path('api/', include(router.urls)),
    
    # Adding URL patterns for JWT authentication to allow users to obtain and refresh tokens for secure access to our API endpoints. This ensures that only authenticated users can interact with our API resources, providing an additional layer of security for our application.
    # ---------------------------------------------------------------
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
