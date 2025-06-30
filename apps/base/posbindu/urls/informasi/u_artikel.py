from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from ...views.informasi.v_artikel import ArtikelListView,DetailArtikelView,AddArtikelView,UpdateArtikelView,ValidasiArtikelView,DeleteArtikelView
app_name ='artikel'
urlpatterns = [
    path('', ArtikelListView.as_view(), name='artikel'),
    path('add/', AddArtikelView.as_view(), name='add_artikel'),
    path('detail/<int:id>/', DetailArtikelView.as_view(), name='detail_artikel'),
    path('validasi/<int:id>/', ValidasiArtikelView.as_view(), name='validasi_artikel'),
    path('edit/<int:id>/', UpdateArtikelView.as_view(), name='edit_artikel'),
    path('update/<int:id>/', UpdateArtikelView.as_view(), name='update_artikel'),
    path('delete/<int:id>/', DeleteArtikelView.as_view(), name='delete_artikel'),
    # ... other URL patterns
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
