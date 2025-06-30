from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from ...views.laporan.v_laporan_sdp import LaporanSdpListView,UpdateLaporanSdpView,DeleteLaporanSdpView,SdpListView,DetailSdpView,UpdateSdpView,DeleteSdpView
app_name ='sdp'
urlpatterns = [
    path('', LaporanSdpListView.as_view(), name='sdp_list'),
    path('add/', LaporanSdpListView.as_view(), name='add_sdp'),
    path('edit/<int:id>/', UpdateLaporanSdpView.as_view(), name='edit_sdp'),
    path('update/<int:id>/', UpdateLaporanSdpView.as_view(), name='update_sdp'),
    path('delete/<int:id>/', DeleteLaporanSdpView.as_view(), name='delete_sdp'),
    # ... other URL patterns
    path('data_sdp/', SdpListView.as_view(), name='data_sdp'),
    path('data_sdp/add/', SdpListView.as_view(), name='add_data_sdp'),
    path('data_sdp/detail/<str:kode>/', DetailSdpView.as_view(), name='detail_data_sdp'),
    path('data_sdp/edit/<int:id>/', UpdateSdpView.as_view(), name='edit_data_sdp'),
    path('data_sdp/update/<int:id>/', UpdateSdpView.as_view(), name='update_data_sdp'),
    path('data_sdp/delete/<int:id>/', DeleteSdpView.as_view(), name='delete_data_sdp'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
