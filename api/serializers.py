from rest_framework import serializers
from django.contrib.auth import get_user_model
from employees.models import DynamicForm, Employee

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 
                  'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'phone_number', 'date_of_birth', 'address']
        read_only_fields = ['id']

class DynamicFormSerializer(serializers.ModelSerializer):
    """Serializer for dynamic forms"""
    created_by = UserSerializer(read_only=True)
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DynamicForm
        fields = ['id', 'name', 'description', 'fields_config', 'created_by', 
                  'created_at', 'updated_at', 'is_active', 'employee_count']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def get_employee_count(self, obj):
        return obj.employees.filter(is_active=True).count()
    
    def validate_fields_config(self, value):
        """Validate fields configuration structure"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Fields config must be a list")
        
        for field in value:
            if not isinstance(field, dict):
                raise serializers.ValidationError("Each field must be a dictionary")
            if 'name' not in field or 'type' not in field or 'label' not in field:
                raise serializers.ValidationError(
                    "Each field must have 'name', 'type', and 'label' keys"
                )
        
        return value

class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for employees"""
    form = DynamicFormSerializer(read_only=True)
    form_id = serializers.PrimaryKeyRelatedField(
        queryset=DynamicForm.objects.filter(is_active=True),
        source='form',
        write_only=True
    )
    created_by = UserSerializer(read_only=True)
    display_name = serializers.CharField(source='get_display_name', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'form', 'form_id', 'employee_data', 'created_by', 
                  'created_at', 'updated_at', 'is_active', 'display_name']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def validate_employee_data(self, value):
        """Validate employee data against form fields"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Employee data must be a dictionary")
        return value

class EmployeeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for employee listing"""
    form_name = serializers.CharField(source='form.name', read_only=True)
    display_name = serializers.CharField(source='get_display_name', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'form_name', 'display_name', 'created_at', 'is_active']