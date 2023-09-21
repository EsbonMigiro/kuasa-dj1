from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),
]

# Configure Admin Titles
admin.site.site_header = "Kuasa Admins"
admin.site.site_title = "KUASA"
admin.site.site_url = "https://kuasa.live"
admin.site.index_title = "Welcome"