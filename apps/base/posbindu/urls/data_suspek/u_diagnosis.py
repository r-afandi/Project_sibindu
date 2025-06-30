from django.urls import path,include
from ...views.data_suspek.v_diagnosis import DiagnosisView
app_name ='diagnosis'
urlpatterns = [
    path('diagnosis/', DiagnosisView.as_view(), name='diagnosis'),
    path("registrasi/", include("apps.base.posbindu.urls.data_suspek.diagnosis.u_registrasi")),
    path("pelacakan_gejala/", include("apps.base.posbindu.urls.data_suspek.diagnosis.u_pelacakan_gejala")),
    path("pengecekan_luar/", include("apps.base.posbindu.urls.data_suspek.diagnosis.u_pengecekan_luar")),
    path("pengecekan_dalam/", include("apps.base.posbindu.urls.data_suspek.diagnosis.u_pengecekan_dalam")),
    path("penanganan/", include("apps.base.posbindu.urls.data_suspek.diagnosis.u_penanganan")),

]

