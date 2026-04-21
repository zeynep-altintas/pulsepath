from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Stores each user's personal artist selections (by name)
class PersonalLineup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    selected_artists = models.JSONField(default=list)  # e.g. ["Billie Eilish", "Fred again.."]

    def __str__(self):
        return f"{self.user.username}'s Lineup"

# Represents a stage or facility on the festival map
class Facility(models.Model):
    CATEGORY_CHOICES = [
        ('stage', 'Stage'),
        ('bathroom', 'Bathroom'),
        ('water', 'Water Station'),
        ('food', 'Food Stall'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

# Links a user account to an organiser profile flag
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_organiser = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"

# Automatically creates a Profile if one doesn't exist when a User is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
