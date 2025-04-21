# mini_project_2/api_docs.py
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Resume Analyzer API",
      default_version='v1',
      description="AI-Powered Resume Analysis Platform API Documentation",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="magzhan1501@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)