from django.urls import path
from ...views.data_suspek.v_data_suspek import DataSuspekListView,DataSuspekView,PrintDataSuspekView,UpdateDataSuspekView,DeleteDataSuspekView,LaporanDataSuspekView,CetakSuspekView
app_name ='data_suspek'
urlpatterns = [
    path('', DataSuspekListView.as_view(), name='data_suspek'),
    path('add/', DataSuspekListView.as_view(), name='add_suspek'),
    path('view/<str:nik>/', DataSuspekView.as_view(), name='view_suspek'),
    path('print/<int:id>/', PrintDataSuspekView.as_view(), name='print_suspek'),
    path('edit/<int:id>/', UpdateDataSuspekView.as_view(), name='edit_suspek'),
    path('update/<int:id>/', UpdateDataSuspekView.as_view(), name='update_suspek'),
    path('delete/<int:id>/', DeleteDataSuspekView.as_view(), name='delete_suspek'),
    path('laporan/', LaporanDataSuspekView.as_view(), name='laporan_data_suspek'),
    path('cetak-suspek/', CetakSuspekView.as_view(), name='cetak_suspek'),
    
    # ... other URL patterns
]
