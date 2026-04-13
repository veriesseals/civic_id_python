"""
URL configuration for civicid project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.persons.views import PersonViewSet
from apps.birth_records.views import BirthRecordViewSet
from apps.audit.views import AuditLogViewSet
from apps.id_applications.views import IDApplicationViewSet
from apps.issued_ids.views import IssuedIDViewSet
from apps.immigration_status.views import ImmigrationStatusViewSet
from apps.naturalization.views import NaturalizationRecordViewSet

# ── API Router ──────────────────────────────────────────────────
router = DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'birth-records', BirthRecordViewSet)
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'id-applications', IDApplicationViewSet)
router.register(r'issued-ids', IssuedIDViewSet)
router.register(r'immigration-status', ImmigrationStatusViewSet)
router.register(r'naturalization', NaturalizationRecordViewSet)

# ── URL Patterns ─────────────────────────────────────────────────
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/law-enforcement/', include('apps.law_enforcement.urls')),

    # ── Frontend pages served by Django ─────────────────────────
    # Login / root
    path('', TemplateView.as_view(template_name='index.html'), name='login'),

    # Inner pages — all live under /pages/<name>/
    path('pages/dashboard/', TemplateView.as_view(template_name='pages/dashboard.html'), name='dashboard'),
    path('pages/persons/', TemplateView.as_view(template_name='pages/persons.html'), name='persons'),
    path('pages/birth-records/', TemplateView.as_view(template_name='pages/birth-records.html'), name='birth-records'),
    path('pages/id-applications/', TemplateView.as_view(template_name='pages/id-applications.html'), name='id-applications'),
    path('pages/audit/', TemplateView.as_view(template_name='pages/audit.html'), name='audit'),
    path('pages/law-enforcement/', TemplateView.as_view(template_name='pages/law-enforcement.html'), name='law-enforcement'),
    path('pages/immigration/', TemplateView.as_view(template_name='pages/immigration.html'), name='immigration'),
    path('pages/issued-ids/', TemplateView.as_view(template_name='pages/issued-ids.html'), name='issued-ids'),
]

# Serve media files (logo, images) in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)