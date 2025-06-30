from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("data_suspek/", include("apps.base.posbindu.urls.data_suspek.u_data_suspek")),
    path("laporan/kegiatan/", include("apps.base.posbindu.urls.laporan.u_laporan_kegiatan")),
    path("laporan/sdp/", include("apps.base.posbindu.urls.laporan.u_laporan_sdp")),
    path("informasi/artikel/", include("apps.base.posbindu.urls.informasi.u_artikel")),
    path("informasi/pengumuman/", include("apps.base.posbindu.urls.informasi.u_pengumuman")),
    path("user/", include("apps.base.posbindu.urls.u_user")),
    path("tentang/", include("apps.base.posbindu.urls.u_about")),
    path("diagnosis/", include("apps.base.posbindu.urls.data_suspek.u_diagnosis")),
    # ... other URL patterns

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
