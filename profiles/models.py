from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Wine


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    # Relationships
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Fields
    default_full_name = models.CharField(max_length=40, null=True, blank=True)
    default_phone_number = (
        models.CharField(max_length=15, null=True, blank=True))
    default_street_address1 = (
        models.CharField(max_length=80, null=True, blank=True))
    default_street_address2 = (
        models.CharField(max_length=80, null=True, blank=True))
    default_town_or_city = (
        models.CharField(max_length=40, null=True, blank=True))
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = (
        CountryField(blank_label='Country', null=True, blank=True))

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()


class Favourite(models.Model):
    """
    A user profile model for users to add favourites.
    """

    # Relationships
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favourited_by')
    wine = models.ForeignKey(
        Wine, on_delete=models.CASCADE, related_name='favourites')

    # Fields
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'wine')

    def __str__(self):
        return f"{self.user.username} favourited {self.wine.name}"
