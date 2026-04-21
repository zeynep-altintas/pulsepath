from django.contrib import admin
from django.urls import path, include
from map import views as map_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('map.urls')),  # Includes all main routes: map, lineup, dashboard, etc.
    path('accounts/', include('django.contrib.auth.urls')),  # Django login/logout views
    path('signup/', map_views.signup_view, name='signup'),   # Custom signup
]
