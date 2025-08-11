


## App Structure (Essentials)

project_root/
├── device_health/    # Django project settings
├── health/           # Main app (models, views, templates)
├── manage.py         # Django management script
└── requirements.txt  # Python dependencies


### Key files for device management views:
- health/views.py              # All class-based views and access control
- health/urls.py               # URL routing for device views
- health/templates/health/device_list.html   # Main device table UI
- health/templates/health/device_row.html    # Partial for device row (display & inline edit)

### Class-based views for device management:
- DeviceListView: Renders the main device table for a given platform (GET only, superadmin required)
- DeviceInlineEditView: Handles inline editing of a device row (GET returns edit form, POST saves changes and returns updated row)
- DeviceRowView: Returns a single device row in display mode (used for Cancel action)

All device management views use Django class-based views with a SuperAdminRequiredMixin for access control. Inline editing is handled by HTMX requests to these views, which return partial templates for seamless updates.

### Models and Platform-specific handling:
- Each platform (Windows, Android) has its own Device and DeviceStatus models
- Device models include: ip_address, mac_address, hostname, location fields
- DeviceStatus models track online status separately
- UserRole model enforces superadmin access control

### Key implementation details:
- CSRF: Hidden token in device_list.html + HTMX event listener for all requests
- DataTables: Initialized on #device-table with default configuration
- Inline editing: Uses colspan=6 in device_row.html for proper table layout
- Device row updates: HTMX targets tr#device-{id} with outerHTML swap

### Platform handling pattern:
```python
# Central helper function for platform-specific logic
def get_device_by_platform(platform, pk=None):
    if platform == 'windows':
        return WindowsDevice if pk is None else get_object_or_404(WindowsDevice, pk=pk)
    elif platform == 'android':
        return AndroidDevice if pk is None else get_object_or_404(AndroidDevice, pk=pk)
    else:
        raise HttpResponseForbidden('Unknown platform')
```

### URLs pattern:
- List: /health/<platform>/
- Inline edit: /health/<platform>/edit-inline/<id>/
- Row view: /health/<platform>/row/<id>/

### Code organization:
- DRY: Platform logic centralized in helper function
- Composable: SuperAdminRequiredMixin for access control
- Flexible: Easy to add new platforms
- Clean: No Django forms, direct POST handling
- Efficient: Uses select_related for status lookups

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->


This project is a Django app for managing devices across multiple platforms (e.g., Windows, Android) with:
- HTMX for AJAX/inline editing (no page reloads, custom row editing, and partial updates)
- Bootstrap 5 for all UI styling
- DataTables for table display (sorting, filtering, pagination)
- Each platform has its own device and status models
- Only superadmins (checked via session and UserRole) can access the main views
- Inline editing is implemented using HTMX: clicking Edit on a row swaps it to a form, Save updates and swaps back, Cancel restores the row
- All device editing is done inline in the table, not in a modal
- CSRF protection is handled for all HTMX requests
- Code should be modular, DRY, and easy to extend for new platforms (add new device/status models, views, and templates with minimal duplication)

When generating code, follow these principles:
- Use class-based views and mixins for access control
- Use partial templates for device rows and forms
- Keep platform-specific logic isolated and easy to extend
- Prefer open-source, maintainable solutions (no proprietary DataTables Editor)
- Ensure all UI is responsive and accessible
