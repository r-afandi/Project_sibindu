from django.urls import path, include


urlpatterns = [
    path("data_pakar/", include("apps.base.expert.urls.data_pakar.u_data_pakar")),
    path("data_diagnosa/", include("apps.base.expert.urls.data_diagnosa.u_data_diagnosa")),

    # ... other URL patterns
]