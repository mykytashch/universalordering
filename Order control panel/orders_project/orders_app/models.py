from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models import JSONField

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import EmailValidator
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
    email = models.EmailField(unique=True, validators=[EmailValidator(message="Invalid email")])  # Using EmailValidator for validation
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
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the first name of the user."""
        return self.first_name


THEME_CHOICES = [  # Добавляем определение THEME_CHOICES
    ('light', 'Light'),
    ('dark', 'Dark'),
]


class TextEntry(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50] + "..." if len(self.text) > 50 else self.text


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    theme_preference = models.CharField(max_length=20, choices=THEME_CHOICES, default='light')

    def __str__(self):
        return self.user.email

class InvitationCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    is_used = models.BooleanField(default=False)
    expiration_date = models.DateTimeField()

    @staticmethod
    def generate_unique_code():
        """Generate a unique 10-character code."""
        while True:
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            if not InvitationCode.objects.filter(code=code).exists():
                return code

    def set_expiration(self, hours=24):
        """Set the expiration date for the code."""
        self.expiration_date = timezone.now() + timezone.timedelta(hours=hours)
        self.save()



class Order(models.Model):
    RECOGNIZED = 'recognized'
    UNRECOGNIZED = 'unrecognized'
    STATUS_CHOICES = [
        (RECOGNIZED, 'Recognized'),
        (UNRECOGNIZED, 'Unrecognized')
    ]

    customer_name = models.CharField(max_length=255, blank=True, null=True)  # Name of the customer
    product = models.CharField(max_length=255, blank=True, null=True)  # Product ordered by the customer
    unrecognized_data = models.TextField(blank=True, null=True)  # Data for orders that couldn't be recognized
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=RECOGNIZED)  # Status of the order: recognized or unrecognized
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time when the order was created
    updated_at = models.DateTimeField(auto_now=True)  # Date and time when the order was last updated
# Обязательные поля
    dmn = models.CharField(max_length=255, blank=True, null=True)
    oid = models.PositiveIntegerField(blank=True, null=True)

    # Дополнительные переменные
    uid = models.PositiveIntegerField(blank=True, null=True)
    dt = models.DateTimeField(blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    itm = JSONField(blank=True, null=True)
    pmt = models.CharField(max_length=50, blank=True, null=True)
    amt = models.FloatField(blank=True, null=True)
    shp = JSONField(blank=True, null=True)
    disc = models.CharField(max_length=100, blank=True, null=True)
    eml = models.EmailField(blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    addr = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    cur = models.CharField(max_length=3, blank=True, null=True)
    sts = models.CharField(max_length=50, blank=True, null=True)
    rfid = models.PositiveIntegerField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    geo = JSONField(blank=True, null=True)
    brw = models.CharField(max_length=50, blank=True, null=True)
    os = models.CharField(max_length=50, blank=True, null=True)
    aff = models.PositiveIntegerField(blank=True, null=True)
    crt = JSONField(blank=True, null=True)
    src = models.CharField(max_length=100, blank=True, null=True)
    loy = JSONField(blank=True, null=True)
    rev = JSONField(blank=True, null=True)
    sub = JSONField(blank=True, null=True)
    gdr = models.CharField(max_length=10, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    prfl = JSONField(blank=True, null=True)
    hist = JSONField(blank=True, null=True)
    fav = JSONField(blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    col = models.CharField(max_length=50, blank=True, null=True)
    wgt = models.FloatField(blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    cat = models.CharField(max_length=100, blank=True, null=True)
    dur = models.PositiveIntegerField(blank=True, null=True)
    rat = models.FloatField(blank=True, null=True)
    view = models.PositiveIntegerField(blank=True, null=True)
    lstv = models.DateTimeField(blank=True, null=True)
    wishlist = JSONField(blank=True, null=True)
    cartab = models.PositiveIntegerField(blank=True, null=True)
    refurl = models.URLField(blank=True, null=True)
    churn = models.FloatField(blank=True, null=True)
    camp = models.CharField(max_length=100, blank=True, null=True)
    coupon = models.CharField(max_length=50, blank=True, null=True)
    pltf = models.CharField(max_length=50, blank=True, null=True)
    mems = models.CharField(max_length=50, blank=True, null=True)
    srchq = models.CharField(max_length=255, blank=True, null=True)
    shipm = models.CharField(max_length=100, blank=True, null=True)
    ret = JSONField(blank=True, null=True)
    lang = models.CharField(max_length=10, blank=True, null=True)
    nviews = models.PositiveIntegerField(blank=True, null=True)
    feedb = JSONField(blank=True, null=True)
    lgnmth = models.CharField(max_length=50, blank=True, null=True)
    dev = models.CharField(max_length=100, blank=True, null=True)
    pricetg = models.CharField(max_length=50, blank=True, null=True)
    recprod = models.BooleanField(default=False)
    fit = models.BooleanField(default=False)
    stk = models.CharField(max_length=50, blank=True, null=True)
    adgrp = models.CharField(max_length=100, blank=True, null=True)
    vchat = models.BooleanField(default=False)
    vtry = models.BooleanField(default=False)
    abtest = models.BooleanField(default=False)
    vidrev = models.BooleanField(default=False)
    pback = models.BooleanField(default=False)
    mktseg = models.CharField(max_length=100, blank=True, null=True)
    intnt = models.CharField(max_length=50, blank=True, null=True)
    push = models.BooleanField(default=False)
    app = models.BooleanField(default=False)
    loytier = models.CharField(max_length=50, blank=True, null=True)
    smshare = models.BooleanField(default=False)
    repbuy = models.BooleanField(default=False)
    gtway = models.CharField(max_length=50, blank=True, null=True)
    savwl = models.BooleanField(default=False)
    hlpdesk = models.BooleanField(default=False)
    custseg = models.CharField(max_length=50, blank=True, null=True)
    dlvryex = JSONField(blank=True, null=True)
    prodsrc = models.CharField(max_length=100, blank=True, null=True)
    paylatr = models.BooleanField(default=False)
    charity = models.BooleanField(default=False)
    def __str__(self):
        return self.customer_name or 'Unrecognized Order'




class BaseOrder(models.Model):
    RECOGNIZED = 'recognized'
    UNRECOGNIZED = 'unrecognized'
    STATUS_CHOICES = [
        (RECOGNIZED, 'Recognized'),
        (UNRECOGNIZED, 'Unrecognized')
    ]

    customer_name = models.CharField(max_length=255, blank=True, null=True)
    product = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=RECOGNIZED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.customer_name or 'Order'

class RecognizedOrder(BaseOrder):
    pass

class UnrecognizedOrder(BaseOrder):
    unrecognized_data = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Unrecognized Order - {self.id}'

class Comment(models.Model):
    text = models.TextField()

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recognized_order = models.ForeignKey(RecognizedOrder, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    unrecognized_order = models.ForeignKey(UnrecognizedOrder, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
