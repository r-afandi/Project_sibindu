from django.urls import path
from ....views.data_suspek.diagnosis.v_pengecekan_luar import PengecekanLuar,UpdatePengecekanLuar
app_name ='pengecekan_luar'
urlpatterns = [
    path('', PengecekanLuar.as_view(),name='pengecekan_luar'),
    path('edit/<int:id>/', UpdatePengecekanLuar.as_view(),name='edit_pengecekan_luar'),
    path('update/<int:id>/', UpdatePengecekanLuar.as_view(),name='update_pengecekan_luar'),
]

