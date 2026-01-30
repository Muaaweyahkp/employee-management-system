from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

# Create router for viewsets
router = DefaultRouter()
router.register(r'forms', views.DynamicFormViewSet, basename='api-form')
router.register(r'employees', views.EmployeeViewSet, basename='api-employee')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register_api, name='api-register'),
    path('auth/login/', views.login_api, name='api-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('auth/profile/', views.user_profile_api, name='api-profile'),
    
    # Include router URLs
    path('', include(router.urls)),
]