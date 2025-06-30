from django.urls import path
from ..views.v_user import UserListView,UpdateUserView,DeleteUserView,ProfilListView,WilayahKerjaListView,UpdateWilayahKerjaView,DeleteWilayahKerjaView
app_name ='user'
urlpatterns = [
    path('', UserListView.as_view(), name='user'),
    path('add/', UserListView.as_view(), name='add_user'),
    path('edit/<int:id>/', UpdateUserView.as_view(), name='edit_user'),
    path('update/<int:id>/', UpdateUserView.as_view(), name='update_user'),
    path('delete/<int:id>/', DeleteUserView.as_view(), name='delete_user'),
    # ... other URL patterns
    path('profil/', ProfilListView.as_view(), name='profil'),
    path('profil/update/', ProfilListView.as_view(), name='update_profil'),
    path('profil/wilayah_kerja/', ProfilListView.as_view(), name='delete_profil'),
    #wilayah kerja
    path('wilayah_kerja/', WilayahKerjaListView.as_view(), name='wilayah_kerja'),
    path('wilayah_kerja/add/', WilayahKerjaListView.as_view(), name='add_wilayah_kerja'),
    path('wilayah_kerja/edit/<int:id>/', UpdateWilayahKerjaView.as_view(), name='edit_wilayah_kerja'),
    path('wilayah_kerja/update/<int:id>/', UpdateWilayahKerjaView.as_view(), name='update_wilayah_kerja'),
    path('wilayah_kerja/delete/<int:id>/', DeleteWilayahKerjaView.as_view(), name='delete_wilayah_kerja'),
]
