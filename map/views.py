from django.shortcuts import render, redirect
from django.conf import settings
from django.templatetags.static import static
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import LoginView, LogoutView

from rest_framework.decorators import api_view
from rest_framework.response import Response

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Facility, PersonalLineup, Profile

import json, csv, random, requests

# Checks if a user is an organiser (used in @user_passes_test)
def is_organiser(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_organiser

# Custom login view that ensures a Profile is created on login
class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.get_or_create(user=self.request.user)
        return response

# Custom logout view that displays a toast message
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You’ve been successfully logged out. See you again soon!")
        return super().dispatch(request, *args, **kwargs)

# User signup view with optional organiser toggle
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        is_organiser = request.POST.get('is_organiser') == 'on'

        if form.is_valid():
            user = form.save()
            user.profile.is_organiser = is_organiser
            user.profile.save()
            login(request, user)
            messages.success(request, "Welcome to PulsePath! Your account has been created.")
            return redirect('personal_lineup')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Renders the full lineup page and saves selected artists
def lineup_view(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        selected_artists = request.POST.get("selected_artists")
        if selected_artists:
            selected_list = json.loads(selected_artists)
            PersonalLineup.objects.update_or_create(
                user=request.user,
                defaults={"selected_artists": selected_list}
            )
            messages.success(request, "Your personal lineup has been saved!")
        return redirect('personal_lineup')

    return render(request, 'pulsepath/lineup.html', {
        "artist_lineup": ARTIST_LINEUP
    })

# Filters the lineup to show only selected artists
@login_required
def personal_lineup_view(request):
    saved = PersonalLineup.objects.filter(user=request.user).first()
    selected_names = saved.selected_artists if saved else []

    filtered = [artist for artist in ARTIST_LINEUP if artist['name'] in selected_names]

    return render(request, 'pulsepath/personal_lineup.html', {
        "artist_lineup": filtered
    })

# Static info pages
def about_view(request):
    return render(request, 'pulsepath/about.html')

def landing_view(request):
    return render(request, 'pulsepath/landing.html')

# Renders the interactive map and passes required JSON context
def map_view(request):
    facilities = list(Facility.objects.values("name", "category", "latitude", "longitude"))
    facilities_json = json.dumps(facilities)

    if isinstance(request.user, AnonymousUser) or not request.user.is_authenticated:
        selected_artists = []
    else:
        user_lineup = PersonalLineup.objects.filter(user=request.user).first()
        selected_artists = user_lineup.selected_artists if user_lineup else []

    selected_stages = [
        artist["stage"]
        for artist in ARTIST_LINEUP
        if artist["name"] in selected_artists
    ]

    return render(request, 'map/map.html', {
        'mapbox_token': settings.MAPBOX_ACCESS_TOKEN,
        'facilities_json': facilities_json,
        'stage_icon_url': static('icons/stage.png'),
        'bathroom_icon_url': static('icons/toilet.png'),
        'water_icon_url': static('icons/water-tap.png'),
        'food_icon_url': static('icons/restaurant.png'),
        'compass_icon_url': static('icons/compass.png'),
        'user_stages_json': json.dumps(selected_stages),
        'artist_lineup_json': json.dumps(ARTIST_LINEUP),
        'selected_artists_json': json.dumps(selected_artists),
    })

# Festival geofences for capacity tracking
GEOFENCES = [
    {'name': 'Main Pulse', 'min_lat': 53.3825, 'max_lat': 53.383, 'min_lon': -6.263, 'max_lon': -6.2625},
    {'name': 'Bassment Bloom', 'min_lat': 53.382, 'max_lat': 53.3825, 'min_lon': -6.263, 'max_lon': -6.2625},
    {'name': 'The Glade', 'min_lat': 53.3815, 'max_lat': 53.382, 'min_lon': -6.263, 'max_lon': -6.2625},
    {'name': 'Toilets East', 'min_lat': 53.3823, 'max_lat': 53.3826, 'min_lon': -6.2614, 'max_lon': -6.2611},
    {'name': 'Toilets West', 'min_lat': 53.3823, 'max_lat': 53.3826, 'min_lon': -6.2643, 'max_lon': -6.264},
    {'name': 'Food Court', 'min_lat': 53.3829, 'max_lat': 53.3832, 'min_lon': -6.2623, 'max_lon': -6.262},
    {'name': 'Water Station', 'min_lat': 53.3836, 'max_lat': 53.3838, 'min_lon': -6.2615, 'max_lon': -6.2613},
]

user_geofence_map = {}

# Utility function to check if a location is inside a geofence
def is_inside_geofence(lat, lon, geofence):
    return (
        geofence['min_lat'] <= lat <= geofence['max_lat'] and
        geofence['min_lon'] <= lon <= geofence['max_lon']
    )

# API endpoint to receive user location and broadcast zone counts
@api_view(['POST'])
def update_user_location(request):
    user_id = request.data.get('user_id')
    lat = float(request.data.get('latitude'))
    lon = float(request.data.get('longitude'))

    if not user_id or lat is None or lon is None:
        return Response({'error': 'user_id, latitude, and longitude are required'}, status=400)

    current_zone = None
    for geofence in GEOFENCES:
        if is_inside_geofence(lat, lon, geofence):
            current_zone = geofence['name']
            break

    user_geofence_map[user_id] = current_zone

    zone_counts = {
        geo['name']: list(user_geofence_map.values()).count(geo['name'])
        for geo in GEOFENCES
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "room_crowd_updates",
        {"type": "crowd_message", "message": {"zone_counts": zone_counts}}
    )

    return Response({'user_zone': current_zone, 'zone_counts': zone_counts})

# Static artist lineup used across pages
ARTIST_LINEUP = [
    {"name": "Billie Eilish", "stage": "Main Pulse", "time": "21:00"},
    {"name": "Fred again..", "stage": "Bassment Bloom", "time": "22:30"},
    {"name": "Nia Archives", "stage": "The Glade", "time": "20:00"},
    {"name": "Barry Can't Swim", "stage": "The Glade", "time": "18:30"},
    {"name": "Arlo Parks", "stage": "Main Pulse", "time": "17:15"},
    {"name": "Confidence Man", "stage": "The Glade", "time": "16:00"},
    {"name": "Loyle Carner", "stage": "Bassment Bloom", "time": "15:30"},
    {"name": "CMAT", "stage": "Main Pulse", "time": "14:00"},
]

# Admin dashboard with dummy footfall and stall visit stats
@login_required
@user_passes_test(is_organiser)
def dashboard_view(request):
    peak_footfall = {
        'Main Pulse': 220,
        'Bassment Bloom': 175,
        'The Glade': 200
    }
    stall_visits = {
        'Toilets': 560,
        'Food Vendors': 410,
        'Water Stations': 300
    }
    return render(request, 'pulsepath/dashboard.html', {
        'peak_footfall': peak_footfall,
        'stall_visits': stall_visits
    })

# Simulates user movement and broadcasts fake crowd data
@api_view(['POST'])
@user_passes_test(is_organiser)
def simulate_festival_crowd(request):
    ZONES = [g['name'] for g in GEOFENCES]
    fake_users = [f"user{i}" for i in range(1, 41)]  # 40 fake users

    zone_weights = {
        'Main Pulse': 0.25, 'Bassment Bloom': 0.2, 'The Glade': 0.2,
        'Toilets East': 0.1, 'Toilets West': 0.1, 'Food Court': 0.1, 'Water Station': 0.05
    }

    weighted_zones = random.choices(ZONES, weights=[zone_weights[z] for z in ZONES], k=40)

    for user_id, zone in zip(fake_users, weighted_zones):
        geo = next(g for g in GEOFENCES if g['name'] == zone)
        lat = round(random.uniform(geo['min_lat'], geo['max_lat']), 6)
        lon = round(random.uniform(geo['min_lon'], geo['max_lon']), 6)
        requests.post("http://127.0.0.1:8000/update-location/", json={
            "user_id": user_id,
            "latitude": lat,
            "longitude": lon
        })

    return JsonResponse({"status": "success"})

# CSV export of organiser stats and dummy notifications
@login_required
@user_passes_test(is_organiser)
def export_dashboard_data(request):
    footfall = {
        'Main Pulse': 220,
        'Bassment Bloom': 175,
        'The Glade': 200
    }
    notifications = [
        {"timestamp": "12:00:01", "message": "Max crowd in Main Pulse! Deploy 2-3 staff"},
        {"timestamp": "12:02:13", "message": "Send 1 staff to The Glade"},
        {"timestamp": "12:05:07", "message": "Food Court is quiet now. No extra staff needed."}
    ]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pulsepath_dashboard_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['--- FOOTFALL STATS ---'])
    writer.writerow(['Zone', 'Attendees'])
    for zone, count in footfall.items():
        writer.writerow([zone, count])

    writer.writerow([])
    writer.writerow(['--- CROWD MOVEMENT ALERTS ---'])
    writer.writerow(['Timestamp', 'Message'])
    for alert in notifications:
        writer.writerow([alert["timestamp"], alert["message"]])

    return response
