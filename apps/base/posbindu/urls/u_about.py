from django.urls import path
from ..views.v_about import AboutView,UpdateAbout
app_name ='about'
urlpatterns = [
    path('', AboutView.as_view(), name='about'),
    path('update/<int:id>/', UpdateAbout.as_view(), name='update_about'),
    # ... other URL patterns
]
