from django.db import models
from django.utils import timezone

class Contact(models.Model):

    full_name = models.CharField(max_length=1024)
    email = models.EmailField()
    subject = models.CharField(max_length=1024)
    message = models.TextField()


    created_at = models.DateTimeField(default=timezone.now)
   
    def __str__(self) -> str:
        return self.full_name