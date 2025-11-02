from django.contrib import admin
from django.urls import path, include
# ...existing imports...

# Add these imports for serving media in dev
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # add this to expose your blog routes at "/"
    # ...existing url patterns (include your app urls etc.)...
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
