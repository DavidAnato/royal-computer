from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('authentication.urls')),
    path('cart/', include('cart_manage.urls')),
    path('blog/', include('blog.urls')),
    path('', include('ecommerce.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
