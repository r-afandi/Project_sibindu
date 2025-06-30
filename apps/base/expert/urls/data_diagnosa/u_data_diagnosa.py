from django.urls import path
from ...views.data_diagnosa.v_data_diagnosa import DiagnosaListView,UpdateDiagnosaView,DeleteDiagnosaView
from ...views.data_diagnosa.v_data_gejala import GejalaListView,UpdateGejalaView,DeleteGejalaView
app_name ='diagnosa'
urlpatterns = [
    #diagnosa
    path('', DiagnosaListView.as_view(), name='diagnosa'),
    path('edit/<int:id>/', UpdateDiagnosaView.as_view(), name='edit_diagnosa'),
    path('update/<int:id>/', UpdateDiagnosaView.as_view(), name='update_diagnosa'),
    path('delete/<int:id>/', DeleteDiagnosaView.as_view(), name='delete_diagnosa'),
    #gejala
    path('gejala/', GejalaListView.as_view(), name='gejala'),
    path('gejala/edit/<int:id>/', UpdateGejalaView.as_view(), name='edit_gejala'),
    path('gejala/update/<int:id>/', UpdateGejalaView.as_view(), name='update_gejala'),
    path('gejala/delete/<int:id>/', DeleteGejalaView.as_view(), name='delete_gejala'),
    # ... other URL patterns
]
