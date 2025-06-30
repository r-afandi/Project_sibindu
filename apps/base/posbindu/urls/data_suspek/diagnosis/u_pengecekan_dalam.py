from django.urls import path
from ....views.data_suspek.diagnosis.v_pengecekan_dalam import PengecekanDalam,UpdatePengecekanDalam
app_name ='pengecekan_dalam'
urlpatterns = [
    path('', PengecekanDalam.as_view(),name='pengecekan_dalam'),
    path('edit/<int:id>/', UpdatePengecekanDalam.as_view(),name='edit_pengecekan_dalam'),
    path('update/<int:id>/', UpdatePengecekanDalam.as_view(),name='update_pengecekan_dalam'),
]

