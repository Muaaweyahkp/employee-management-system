from django.contrib import admin
from .models import DynamicForm, Employee

@admin.register(DynamicForm)
class DynamicFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'form', 'created_by', 'created_at', 'is_active']
    list_filter = ['is_active', 'form', 'created_at']
    search_fields = ['employee_data']
    readonly_fields = ['created_at', 'updated_at']