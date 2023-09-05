from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random
import string



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email_):
        return self.get(email=email_)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()
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


class BaseOrder(models.Model):
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    product = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.customer_name or 'Order'


class RecognizedOrder(BaseOrder):
    # Если у вас будут дополнительные поля только для распознанных заказов, добавьте их здесь
    pass


class UnrecognizedOrder(BaseOrder):
    unrecognized_data = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Unrecognized Order - {self.id}'


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    related_order = models.ForeignKey(RecognizedOrder, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    unrecognized_order = models.ForeignKey(UnrecognizedOrder, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# Оставшиеся модели также остаются без изменений ...