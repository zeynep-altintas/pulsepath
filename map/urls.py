from django.urls import path
from . import views
from .views import (
    update_user_location,
    landing_view,
    dashboard_view,
    export_dashboard_data,
    simulate_festival_crowd,
    CustomLoginView,
    CustomLogoutView
)

urlpatterns = [
    path('', landing_view, name='home'),  # Landing page
    path('map/', views.map_view, name='map'),
    path('update-location/', update_user_location),
    path('lineup/', views.lineup_view, name='lineup'),
    path('my-lineup/', views.personal_lineup_view, name='personal_lineup'),
    path('about/', views.about_view, name='about'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('export-dashboard-data/', export_dashboard_data, name='export_dashboard_data'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path("simulate-festival/", simulate_festival_crowd, name="simulate_festival"),
]