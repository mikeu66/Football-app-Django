from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=250)
    passing_career = models.TextField(null=True)
    rushing_career = models.TextField(null=True)
    receiving_career = models.TextField(null=True)
    defensive_career = models.TextField(null=True)
    scoring_career = models.TextField(null=True)
    