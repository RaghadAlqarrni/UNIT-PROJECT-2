from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Phone Number")
    is_phone_verified = models.BooleanField(default=False, verbose_name="Is Phone Verified")

    USERNAME_FIELD = 'email'  # استخدام البريد الإلكتروني كحقل تسجيل دخول
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']  # الحقول المطلوبة لإنشاء مستخدم

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name} - {self.subject}'