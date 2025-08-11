# Device Health Django Project

This project is a Django-based web application for managing and monitoring devices across multiple platforms (e.g., Windows, Android). It uses HTMX for inline editing, Bootstrap for styling, and DataTables for enhanced table display. Each platform has its own device and status models. Only superadmins (checked via session and a UserRole model) can access the main views.

## Features
- Separate device and status models for each platform
- List and edit device details (except online status)
- HTMX-powered inline row editing
- Bootstrap styling and responsive design
- DataTables for sorting and filtering
- DRY platform handling with helper functions
- Superadmin-only access to main views

## Setup
1. Create and activate a virtual environment (already set up if using VS Code Python tools)
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```sh
   python manage.py migrate
   ```
4. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```
5. Start the development server:
   ```sh
   python manage.py runserver
   ```

## Usage
- Access device lists at `/health/windows/`, `/health/android/`, etc.
- Only superadmins can access these views
- Click 'Edit' to edit a device row inline
- Save updates the device and exits edit mode
- Cancel reverts changes and exits edit mode

## Extending
- To add a new platform:
  1. Create new device and status models
  2. Update `get_device_by_platform` helper in views.py
  3. No other changes needed - views/templates handle all platforms

---

For more details, see the code and comments in the project.
