from re import search
from django.urls import path, include
from ..views import Index,Berita,BeritaSatuan,Pengumuman,PengumumanDetailView,KegitanDetailView,CekDiabetes,Statistik,About, CustomLoginView, CustomLogoutView,Search,Dashboard
from ..required import ProtectedView
app_name='sibindu'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('artikel/', Berita.as_view(), name='berita'),
    path('artikel_satuan/<int:id>/', BeritaSatuan.as_view(), name='berita_satuan'),
    path('pengumuman/', Pengumuman.as_view(), name='pengumuman'),
    path('pengumuman/<int:id>/', PengumumanDetailView.as_view(), name='detail_pengumuman'),
    path('kegiatan/<int:id>/', KegitanDetailView.as_view(), name='detail_kegiatan'),
    path('search_content/', Search.as_view(), name='search_content'),
    path('cek-diabetes/', CekDiabetes.as_view(), name='cek_diabetes'),
    path('feedback/', CekDiabetes.as_view(), name='feedback'),
    path('hasil/', CekDiabetes.as_view(), name='hasil'),
    path('statistik/', Statistik.as_view(), name='statistik'),
    path('tentang/', About.as_view(), name='about'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('protected/', ProtectedView.as_view(), name='protected-view'),

]