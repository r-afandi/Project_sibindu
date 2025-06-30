from django.urls import path
from ....views.data_suspek.diagnosis.v_pelacakan_gejala import PelacakanGejala,UpdatePelacakanGejala
app_name ='pelacakan_gejala'
urlpatterns = [
    path('', PelacakanGejala.as_view(),name='pelacakan_gejala'),
    path('edit/<int:id>/', UpdatePelacakanGejala.as_view(), name='edit_pelacakan_gejala'),
    path('update/<int:id>/', UpdatePelacakanGejala.as_view(), name='update_pelacakan_gejala'),
    path('delete/<int:id>/', UpdatePelacakanGejala.as_view(), name='delete_pelacakan_gejala'),
]
