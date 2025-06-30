from django.urls import path
from ....views.data_suspek.diagnosis.v_registrasi import Registrasi,UpdateRegistrasi,DeleteRegistrasi,search_nik
app_name ='registrasi'
urlpatterns = [
    path('', Registrasi.as_view(),name='registrasi'),
    path('search_nik/', search_nik, name='search_nik'),
    path('add/', Registrasi.as_view(),name='add_registrasi'),
    path('edit/<int:id>/', UpdateRegistrasi.as_view(), name='edit_registrasi'),
    path('update/<int:id>/', UpdateRegistrasi.as_view(), name='update_registrasi'),
    path('delete/<int:id>/', DeleteRegistrasi.as_view(), name='delete_registrasi'),

]

