from django.db import models
from django.utils import timezone

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=250)
    passing_career = models.TextField(null=True)
    rushing_career = models.TextField(null=True)
    receiving_career = models.TextField(null=True)
    defensive_career = models.TextField(null=True)
    scoring_career = models.TextField(null=True)
    created_date = models.DateTimeField('date created', default=timezone.now)
    count = models.IntegerField(default=1)
    position = models.CharField(max_length=4)
    last_team = models.CharField(max_length=50)
