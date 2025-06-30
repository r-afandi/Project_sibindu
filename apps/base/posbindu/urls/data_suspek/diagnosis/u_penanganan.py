from django.urls import path
from ....views.data_suspek.diagnosis.v_penanganan import Penanganan,EditPenanganan,UpdatePenanganan,PrintPenanganan
app_name ='penanganan'
urlpatterns = [
    path('', Penanganan.as_view(),name='penanganan'),
    path('edit/<int:id>/', EditPenanganan.as_view(), name='edit_penanganan'),
    path('print/<int:id>/', PrintPenanganan.as_view(), name='print_penanganan'),
    path('update/<int:id>/', UpdatePenanganan.as_view(), name='update_penanganan'),

]

