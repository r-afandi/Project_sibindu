from django.urls import path
from ...views.informasi.v_pengumuman import PengumumanListView,UpdatePengumumanView,DeletePengumumanView
app_name ='pengumuman'
urlpatterns = [
    path('', PengumumanListView.as_view(), name='pengumuman'),
    path('add/', PengumumanListView.as_view(), name='add_pengumuman'),
    path('edit/<int:id>/', UpdatePengumumanView.as_view(), name='edit_pengumuman'),
    path('update/<int:id>/', UpdatePengumumanView.as_view(), name='update_pengumuman'),
    path('delete/<int:id>/', DeletePengumumanView.as_view(), name='delete_pengumuman'),
    # ... other URL patterns
]
