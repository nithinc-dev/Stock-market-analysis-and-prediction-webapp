from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Stock(models.Model):
    keyword = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.keyword

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='messages', default=1)  # Add default=1 here
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}: {self.content[:20]}'

    class Meta:
        ordering = ['timestamp']
        
class Alert(models.Model):
    email = models.EmailField()
    keyword = models.CharField(max_length=50)
    price = models.PositiveIntegerField()