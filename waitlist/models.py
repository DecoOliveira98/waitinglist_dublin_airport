from django.db import models
from django.utils import timezone

NOTIFICATION_CHOICES = [
    ('email', 'Email'),
]

class Passenger(models.Model):
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=7, default='+353')  # Irlanda como default
    local_phone = models.CharField(max_length=35)
    email = models.EmailField(blank=True, null=True)
    notification_method = models.CharField(max_length=10, choices=NOTIFICATION_CHOICES, default='email')
    guests = models.IntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)
    called = models.BooleanField(default=False)
    called_at = models.DateTimeField(null=True, blank=True)

    @property
    def full_phone(self):
        code = self.country_code if self.country_code.startswith('+') else f"+{self.country_code}"
        return f"{code}{self.local_phone}"

    def __str__(self):
        return f"{self.name} ({self.full_phone}) - Guests: {self.guests}"

class PassengerLog(models.Model):
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    guests = models.IntegerField(default=0)
    time_joined = models.DateTimeField()
    time_called = models.DateTimeField(auto_now_add=True)

    @property
    def full_phone(self):
        code = self.country_code if self.country_code.startswith('+') else f"+{self.country_code}"
        return f"{code}{self.phone}"

    def __str__(self):
        return f"{self.name} - Called at {self.time_called.strftime('%Y-%m-%d %H:%M')}"
