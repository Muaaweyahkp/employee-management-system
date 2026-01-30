from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q

from .serializers import (
    UserRegistrationSerializer, UserSerializer,
    DynamicFormSerializer, EmployeeSerializer, EmployeeListSerializer
)
from employees.models import DynamicForm, Employee

# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    """
    API endpoint for user registration
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    """
    API endpoint for user login with JWT tokens
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Please provide both username and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_api(request):
    """
    Get current user profile
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# Dynamic Form ViewSet
class DynamicFormViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Dynamic Forms
    """
    queryset = DynamicForm.objects.filter(is_active=True)
    serializer_class = DynamicFormSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete"""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(
            {'message': 'Form deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=True, methods=['get'])
    def fields(self, request, pk=None):
        """Get form fields configuration"""
        form = self.get_object()
        return Response({
            'form_id': form.id,
            'form_name': form.name,
            'fields': form.fields_config
        })

# Employee ViewSet
class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Employees
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Employee.objects.filter(is_active=True).select_related('form', 'created_by')
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(employee_data__icontains=search) |
                Q(form__name__icontains=search)
            )
        
        # Filter by form
        form_id = self.request.query_params.get('form_id', None)
        if form_id:
            queryset = queryset.filter(form_id=form_id)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeListSerializer
        return EmployeeSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete"""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(
            {'message': 'Employee deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get employee statistics"""
        total_employees = Employee.objects.filter(is_active=True).count()
        total_forms = DynamicForm.objects.filter(is_active=True).count()
        
        # Get employee count by form
        forms_with_counts = []
        for form in DynamicForm.objects.filter(is_active=True):
            count = form.employees.filter(is_active=True).count()
            forms_with_counts.append({
                'form_id': form.id,
                'form_name': form.name,
                'employee_count': count
            })
        
        return Response({
            'total_employees': total_employees,
            'total_forms': total_forms,
            'forms_breakdown': forms_with_counts
        })