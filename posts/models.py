from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    pub_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=True)
    votes_total = models.IntegerField(default=0)
