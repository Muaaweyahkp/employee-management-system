from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DynamicForm(models.Model):
    """
    Model to store custom form templates
    """
    FIELD_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('email', 'Email'),
        ('date', 'Date'),
        ('password', 'Password'),
        ('textarea', 'Text Area'),
        ('tel', 'Phone Number'),
        ('url', 'URL'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    fields_config = models.JSONField(default=list)  # Store field configurations as JSON
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'dynamic_form'
        ordering = ['-created_at']
        verbose_name = 'Dynamic Form'
        verbose_name_plural = 'Dynamic Forms'

class Employee(models.Model):
    """
    Model to store employee records with dynamic data
    """
    id = models.AutoField(primary_key=True)
    form = models.ForeignKey(DynamicForm, on_delete=models.CASCADE, related_name='employees')
    employee_data = models.JSONField(default=dict)  # Store all dynamic field values
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Employee #{self.id} - {self.form.name}"
    
    def get_display_name(self):
        """Get a display name from employee data"""
        # Try to find name-like fields
        for key, value in self.employee_data.items():
            if 'name' in key.lower() and value:
                return value
        return f"Employee #{self.id}"
    
    class Meta:
        db_table = 'employee'
        ordering = ['-created_at']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'