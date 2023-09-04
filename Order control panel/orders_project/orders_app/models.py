from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random
import string

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

THEME_CHOICES = [
    ('light', 'Light Theme'),
    ('dark', 'Dark Theme'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    theme_preference = models.CharField(max_length=20, choices=THEME_CHOICES, default='light')

    def __str__(self):
        return self.user.email

class Order(models.Model):
    RECOGNIZED = 'recognized'
    UNRECOGNIZED = 'unrecognized'
    STATUS_CHOICES = [
        (RECOGNIZED, 'Recognized'),
        (UNRECOGNIZED, 'Unrecognized')
    ]

    customer_name = models.CharField(max_length=255, blank=True, null=True)
    product = models.CharField(max_length=255, blank=True, null=True)
    unrecognized_data = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=RECOGNIZED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name or 'Unrecognized Order'

class Comment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="comments", null=True)
    text = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class InvitationCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    is_used = models.BooleanField(default=False)
    expiration_date = models.DateTimeField()

    @staticmethod
    def generate_unique_code():
        while True:
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            if not InvitationCode.objects.filter(code=code).exists():
                return code

    def set_expiration(self, hours=24):
        self.expiration_date = timezone.now() + timezone.timedelta(hours=hours)
        self.save()
