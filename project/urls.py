
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/report/', include('reports.urls')),
    path('api/notifications/', include('notification.urls')),
    path('api/rays/', include('rays.urls')),
    path('api/medicine/', include('medicine.urls')),
    path('api/medical_test/', include('medical_test.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
