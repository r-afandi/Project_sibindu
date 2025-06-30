import os
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from ...views.laporan.v_laporan_kegiatan import KegiatanListView,UpdateKegiatanView,DeleteKegiatanView
app_name ='kegiatan'
urlpatterns = [
    path('', KegiatanListView.as_view(), name='kegiatan'),
    path('add/', KegiatanListView.as_view(), name='add_kegiatan'),
    path('edit/<int:id>/', UpdateKegiatanView.as_view(), name='edit_kegiatan'),
    path('update/<int:id>/', UpdateKegiatanView.as_view(), name='update_kegiatan'),
    path('delete/<int:id>/', DeleteKegiatanView.as_view(), name='delete_kegiatan'),
    # ... other URL patterns
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)