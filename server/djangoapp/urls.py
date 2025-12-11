from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # login API
    path('login', views.login_user, name='login'),

    # logout API (what your JS is calling: /djangoapp/logout)
    path('logout', views.logout_user, name='logout'),
    path('logout/', views.logout_user),  # extra, por si acaso
    path('register', views.register_user, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
