from django.urls import path
from .views import DumpListView, AddDumpView, EditDumpView, UpdateDumpView, DeleteDumpView
app_name ='dump'
urlpatterns = [
    path('', DumpListView.as_view(), name='dump_list'),
    path('add/', AddDumpView.as_view(), name='add_dump'),
    path('edit/<int:id>/', EditDumpView.as_view(), name='edit_dump'),
    path('update/<int:id>/', UpdateDumpView.as_view(), name='update_dump'),
    path('delete/<int:id>/', DeleteDumpView.as_view(), name='delete_dump'),
    # ... other URL patterns
]
