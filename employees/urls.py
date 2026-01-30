from django.urls import path
from . import views

urlpatterns = [
    # Employee URLs
    path('', views.employee_list, name='employee_list'),
    path('create/', views.employee_create, name='employee_create'),
    path('edit/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    
    # Form URLs
    path('forms/', views.form_list, name='form_list'),
    path('forms/create/', views.form_create, name='form_create'),
    path('forms/edit/<int:pk>/', views.form_edit, name='form_edit'),
    path('forms/delete/<int:pk>/', views.form_delete, name='form_delete'),
    
    # AJAX endpoints
    path('api/form-fields/<int:form_id>/', views.get_form_fields, name='get_form_fields'),
]