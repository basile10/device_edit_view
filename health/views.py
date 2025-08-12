from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count, Q
from .models import WindowsDevice, AndroidDevice, UserRole

 # Helper function to get device by platform
def get_device_by_platform(platform, pk=None):
    if platform == 'windows':
        return WindowsDevice if pk is None else get_object_or_404(WindowsDevice, pk=pk)
    elif platform == 'android':
        return AndroidDevice if pk is None else get_object_or_404(AndroidDevice, pk=pk)
    else:
        raise HttpResponseForbidden('Unknown platform')

# SuperAdminRequired mixin
class SuperAdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        user_id = request.user.id
        # Only check UserRole model for 'superadmin' role
        if not UserRole.objects.filter(user_id=user_id, role='superadmin').exists():
            return HttpResponseForbidden('Superadmin access required.')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class DeviceInlineEditView(SuperAdminRequiredMixin, View):
    def get(self, request, platform, pk):
        try:
            device = get_device_by_platform(platform, pk)
            return render(request, 'health/device_row.html', {'device': device, 'platform': platform, 'edit': True})
        except HttpResponseForbidden as e:
            return e

    def post(self, request, platform, pk):
        try:
            device = get_device_by_platform(platform, pk)
            device.ip_address = request.POST.get('ip_address', device.ip_address)
            device.mac_address = request.POST.get('mac_address', device.mac_address)
            device.hostname = request.POST.get('hostname', device.hostname)
            device.location = request.POST.get('location', device.location)
            device.save()
# Do NOT pass 'edit' so the row renders in display mode
            return render(request, 'health/device_row.html', {'device': device, 'platform': platform, 'edit': False})
        except HttpResponseForbidden as e:
            return e


@method_decorator(login_required, name='dispatch')
class DashboardView(SuperAdminRequiredMixin, View):
    def get(self, request):
        # Initial load without stats - they'll be loaded via HTMX
        return render(request, 'health/dashboard.html', {'platforms': {}})

@method_decorator(login_required, name='dispatch')
class DashboardStatsView(SuperAdminRequiredMixin, View):
    def get(self, request):
        platforms = {}
        
        # Windows stats
        windows_stats = WindowsDevice.objects.aggregate(
            total=Count('id'),
            online=Count('status', filter=Q(status__is_online=True)),
            offline=Count('status', filter=Q(status__is_online=False) | Q(status__isnull=True))
        )
        platforms['windows'] = windows_stats
        
        # Android stats
        android_stats = AndroidDevice.objects.aggregate(
            total=Count('id'),
            online=Count('status', filter=Q(status__is_online=True)),
            offline=Count('status', filter=Q(status__is_online=False) | Q(status__isnull=True))
        )
        platforms['android'] = android_stats
        
        # If it's an HTMX request, return only the stats partial
        if request.headers.get('HX-Request'):
            return render(request, 'health/partials/dashboard_stats.html', {'platforms': platforms})
        
        # Otherwise return the full dashboard
        return render(request, 'health/dashboard.html', {'platforms': platforms})
class DeviceRowView(SuperAdminRequiredMixin, View):
    def get(self, request, platform, pk):
        try:
            device = get_device_by_platform(platform, pk)
            return render(request, 'health/device_row.html', {'device': device, 'platform': platform})
        except HttpResponseForbidden as e:
            return e

# Platform device list view
@method_decorator(login_required, name='dispatch')
class DeviceListView(SuperAdminRequiredMixin, View):
    def get(self, request, platform):
        try:
            Device = get_device_by_platform(platform)
            devices = Device.objects.all().select_related('status')
            return render(request, 'health/device_list.html', {
                'devices': devices,
                'platform': platform,
            })
        except HttpResponseForbidden as e:
            return e
