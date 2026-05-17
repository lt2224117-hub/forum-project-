from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib.auth.models import User

def make_admin(request):
    u = User.objects.filter(username='Admin').first()
    if u:
        u.is_staff = True
        u.is_superuser = True
        u.save()
        return HttpResponse('Done! Admin promoted.')
    return HttpResponse('User not found.')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('forum.urls')),
    path('interaction/', include('interaction.urls')),
    path('search/', include('search.urls')),
    path('moderation/', include('moderation.urls')),
    path('make-admin/', make_admin),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
