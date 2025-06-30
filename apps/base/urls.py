from django.urls import path, include
from .views import Dashboard,show_notifications,mark_as_read,delete_notification,csrfToken
from .debugging import revert_upload
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', include("apps.base.home.urls_home")),
    path('dashboard/',Dashboard.as_view(),name='dashboard' ),
    path('notifikasi/',show_notifications,name='notifikasi' ),
    path('get-csrf-token/', csrfToken, name='token'),
    path('mark-as-read/<int:id>/', mark_as_read, name='mark_as_read'),
    path('delete-notification/<int:id>/', delete_notification, name='delete_notification'),
    path('expert/', include("apps.base.expert.urls.urls_expert")),
    path('posbindu/', include("apps.base.posbindu.urls.urls_posbindu")),
    path('fp/', include('django_drf_filepond.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)