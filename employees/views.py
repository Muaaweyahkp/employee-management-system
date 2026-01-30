from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
import json

from .models import DynamicForm, Employee

@login_required
def employee_list(request):
    """List all employees with search and filter functionality"""
    employees = Employee.objects.filter(is_active=True).select_related('form', 'created_by')
    forms = DynamicForm.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    form_filter = request.GET.get('form', '')
    
    if search_query:
        # Search in JSON field
        employees = employees.filter(
            Q(employee_data__icontains=search_query) |
            Q(form__name__icontains=search_query)
        )
    
    if form_filter:
        employees = employees.filter(form_id=form_filter)
    
    context = {
        'employees': employees,
        'forms': forms,
        'search_query': search_query,
        'form_filter': form_filter,
    }
    return render(request, 'employees/employee_list.html', context)

@login_required
def employee_create(request):
    """Create new employee using dynamic form"""
    forms = DynamicForm.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form_id = request.POST.get('form_id')
        
        if not form_id:
            return JsonResponse({'success': False, 'error': 'Form selection required'})
        
        try:
            dynamic_form = DynamicForm.objects.get(id=form_id, is_active=True)
            
            # Extract employee data from POST
            employee_data = {}
            for field in dynamic_form.fields_config:
                field_name = field.get('name')
                field_value = request.POST.get(field_name, '')
                employee_data[field_name] = field_value
            
            # Create employee
            employee = Employee.objects.create(
                form=dynamic_form,
                employee_data=employee_data,
                created_by=request.user
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Employee created successfully!',
                    'employee_id': employee.id
                })
            else:
                messages.success(request, 'Employee created successfully!')
                return redirect('employee_list')
                
        except DynamicForm.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Form not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    context = {'forms': forms}
    return render(request, 'employees/employee_create.html', context)

@login_required
def employee_edit(request, pk):
    """Edit existing employee"""
    employee = get_object_or_404(Employee, pk=pk, is_active=True)
    
    if request.method == 'POST':
        try:
            # Extract updated employee data
            employee_data = {}
            for field in employee.form.fields_config:
                field_name = field.get('name')
                field_value = request.POST.get(field_name, '')
                employee_data[field_name] = field_value
            
            employee.employee_data = employee_data
            employee.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Employee updated successfully!'
                })
            else:
                messages.success(request, 'Employee updated successfully!')
                return redirect('employee_list')
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    context = {'employee': employee}
    return render(request, 'employees/employee_edit.html', context)

@login_required
def employee_delete(request, pk):
    """Delete employee (soft delete)"""
    if request.method == 'POST':
        try:
            employee = get_object_or_404(Employee, pk=pk)
            employee.is_active = False
            employee.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Employee deleted successfully!'
                })
            else:
                messages.success(request, 'Employee deleted successfully!')
                return redirect('employee_list')
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return redirect('employee_list')

@login_required
def form_list(request):
    """List all dynamic forms"""
    forms = DynamicForm.objects.filter(is_active=True)
    return render(request, 'employees/form_list.html', {'forms': forms})

@login_required
def form_create(request):
    """Create new dynamic form"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            fields_json = request.POST.get('fields_config')
            
            if not name:
                return JsonResponse({'success': False, 'error': 'Form name required'})
            
            # Parse fields configuration
            fields_config = json.loads(fields_json) if fields_json else []
            
            # Create form
            form = DynamicForm.objects.create(
                name=name,
                description=description,
                fields_config=fields_config,
                created_by=request.user
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Form created successfully!',
                    'form_id': form.id
                })
            else:
                messages.success(request, 'Form created successfully!')
                return redirect('form_list')
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid field configuration'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'employees/form_create.html')

@login_required
def form_edit(request, pk):
    """Edit existing dynamic form"""
    form = get_object_or_404(DynamicForm, pk=pk, is_active=True)
    
    if request.method == 'POST':
        try:
            form.name = request.POST.get('name', form.name)
            form.description = request.POST.get('description', form.description)
            
            fields_json = request.POST.get('fields_config')
            if fields_json:
                form.fields_config = json.loads(fields_json)
            
            form.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Form updated successfully!'
                })
            else:
                messages.success(request, 'Form updated successfully!')
                return redirect('form_list')
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid field configuration'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    context = {'form': form}
    return render(request, 'employees/form_edit.html', context)

@login_required
def form_delete(request, pk):
    """Delete form (soft delete)"""
    if request.method == 'POST':
        try:
            form = get_object_or_404(DynamicForm, pk=pk)
            form.is_active = False
            form.save()
            
            messages.success(request, 'Form deleted successfully!')
            return redirect('form_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('form_list')
    
    return redirect('form_list')

@login_required
@require_http_methods(["GET"])
def get_form_fields(request, form_id):
    """AJAX endpoint to get form fields configuration"""
    try:
        form = DynamicForm.objects.get(id=form_id, is_active=True)
        return JsonResponse({
            'success': True,
            'fields': form.fields_config,
            'form_name': form.name
        })
    except DynamicForm.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Form not found'})