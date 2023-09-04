from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random
import string

class BaseOrder(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class RecognizedOrder(BaseOrder):
    customer_name = models.CharField(max_length=255)
    product = models.CharField(max_length=255)

    def __str__(self):
        return self.customer_name

class UnrecognizedOrder(BaseOrder):
    data = models.TextField()  # Здесь вы можете добавить другие поля, если необходимо

class Order(models.Model):
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    product = models.CharField(max_length=255, blank=True, null=True)
    unrecognized_data = models.TextField(blank=True, null=True)
    is_recognized = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    # Делаем ForeignKey nullable
    unrecognized_order = models.ForeignKey(UnrecognizedOrder, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class InvitationCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    is_used = models.BooleanField(default=False)
    expiration_date = models.DateTimeField()

    @staticmethod
    def generate_unique_code():
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        return code

    def set_expiration(self, hours=24):
        self.expiration_date = timezone.now() + timezone.timedelta(hours=hours)
        self.save()
