# Login App

A simple and secure login application built using Django and Django REST Framework (DRF).

---
 
## Features

- User registration with email and password.
- User authentication and token-based login.
- Password reset and change functionality.
- Secure API endpoints for authentication.
- Clean and modular structure for easy scalability.

---

## Requirements

- Python 3.x
- Django 4.x
- Django REST Framework
- Any additional dependencies (e.g., `djangorestframework-simplejwt` for JWT tokens)

---

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd authify

   ```

## 
## Next feauturs Updates

1. **Enable Admin to Remove Users**

   - Implement functionality that allows admins to remove users via the Django admin panel or an API endpoint.
   - Admins will have the ability to delete any user through the user list view or an API endpoint with the necessary permissions.

2. **Enable User to Activate/Deactivate Account**

   - Add functionality that allows users to activate or deactivate their accounts.
   - This can be achieved by implementing a `is_active` field or providing an endpoint for account deactivation.
   - Admins can also have the ability to activate or deactivate accounts for other users via the Django admin panel or API.


## Next devolepment Updates
   - use JWT instead of TokenAuthentication
    