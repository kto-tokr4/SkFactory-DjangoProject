from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(to=User,
                                on_delete=models.CASCADE)
    email_code = models.IntegerField()

class News(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
