from django.urls import path
from .views import DeviceListView, DeviceInlineEditView, DeviceRowView

app_name = 'health'

urlpatterns = [
    path('<str:platform>/', DeviceListView.as_view(), name='device_list'),
    path('<str:platform>/edit-inline/<int:pk>/', DeviceInlineEditView.as_view(), name='device_edit_inline'),
    path('<str:platform>/row/<int:pk>/', DeviceRowView.as_view(), name='device_row'),
]
