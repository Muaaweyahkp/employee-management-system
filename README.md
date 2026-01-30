# Employee Management System

A Django-based Employee Management System with dynamic form creation, REST API, and JWT authentication.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd employee_management_system
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Web Interface: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API: http://127.0.0.1:8000/api/

## ✨ Features

### Web Interface
- ✅ User Authentication (Login, Register, Logout)
- ✅ Profile Management
- ✅ Password Change
- ✅ Dynamic Form Builder
- ✅ Employee CRUD Operations
- ✅ Search and Filter Functionality
- ✅ AJAX-based Form Submissions

### REST API
- ✅ JWT Authentication (Access & Refresh Tokens)
- ✅ Complete CRUD for Forms and Employees
- ✅ Search and Filter Endpoints
- ✅ Employee Statistics

## 📚 API Testing with Postman

### 1. Import Postman Collection
- Open Postman
- Click **"Import"**
- Select `Employee_Management_API.postman_collection.json`

### 2. Set Environment Variable
- In Postman, click **"Environments"** (left sidebar)
- Click **"Create Environment"** or **"+"**
- Name it: `Employee Management`
- Add variable:
  - Variable: `base_url`
  - Initial Value: `http://127.0.0.1:8000`
  - Current Value: `http://127.0.0.1:8000`
- Click **"Save"**
- **Select this environment** from the dropdown (top-right)

### 3. Test Authentication
- Run **"Register User"** request
- Run **"Login"** request (this will save access token automatically)
- Access token is automatically stored for subsequent requests

### 4. Test Forms API
- Run **"Create Form"** request
- Run **"List All Forms"** request
- Run **"Get Form Details"** request

### 5. Test Employees API
- Run **"Create Employee"** request
- Run **"List All Employees"** request
- Run **"Search Employees"** request
- Run **"Get Employee Statistics"** request

## 📖 API Documentation

### Base URL
```
http://127.0.0.1:8000/api
```

### Authentication Endpoints

#### Register
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "confirm_password": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "securepass123"
}
```

**Response:**
```json
{
    "message": "Login successful",
    "user": {...},
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

### Forms Endpoints

#### Create Form
```http
POST /api/forms/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Employee Registration Form",
    "description": "Standard employee form",
    "fields_config": [
        {
            "name": "full_name",
            "label": "Full Name",
            "type": "text",
            "required": true,
            "order": 0
        }
    ]
}
```

#### List Forms
```http
GET /api/forms/
Authorization: Bearer <access_token>
```

### Employees Endpoints

#### Create Employee
```http
POST /api/employees/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "form_id": 1,
    "employee_data": {
        "full_name": "John Doe",
        "email": "john.doe@example.com"
    }
}
```

#### List Employees
```http
GET /api/employees/
Authorization: Bearer <access_token>

# With search
GET /api/employees/?search=john

# With form filter
GET /api/employees/?form_id=1
```

#### Get Statistics
```http
GET /api/employees/statistics/
Authorization: Bearer <access_token>
```

## 🛠️ Technology Stack

- **Backend:** Django 5.0.1
- **API:** Django REST Framework 3.14.0
- **Authentication:** JWT (djangorestframework-simplejwt 5.3.1)
- **Database:** SQLite (default)
- **Frontend:** HTML, CSS, JavaScript

## 📁 Project Structure

```
employee_management_system/
├── employee_system/          # Main Django project
├── accounts/                 # Authentication app
├── employees/                # Employee management app
├── api/                      # REST API app
├── manage.py
├── requirements.txt
└── Employee_Management_API.postman_collection.json
```

## 🔑 Key Features

- **Dynamic Form System:** Create forms with customizable fields (Text, Number, Email, Date, Password, TextArea, Phone, URL)
- **Employee Management:** CRUD operations with search and filter
- **JWT Authentication:** Secure API access with access and refresh tokens
- **AJAX Forms:** Smooth user experience without page reloads
- **Soft Delete:** Data preservation

## 📝 Notes

- Access tokens expire after 5 hours
- Refresh tokens expire after 1 day
- Soft delete is implemented (data is not permanently deleted)

## 🐛 Troubleshooting

**"401 Unauthorized" in API**
- Ensure Bearer token is included: `Authorization: Bearer <access_token>`

**"No such table" errors**
- Run: `python manage.py makemigrations && python manage.py migrate`

## 👨‍💻 Developer

Developed as part of a machine test project for employee management system with dynamic form capabilities.