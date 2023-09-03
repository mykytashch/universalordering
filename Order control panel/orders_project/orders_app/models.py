from django.db import models
from django.utils import timezone
import random
import string

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


class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.customer_name
