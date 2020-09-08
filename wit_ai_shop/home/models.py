from django.db import models

# Create your models here.

class mobile(models.Model):
    name = models.TextField(max_length=50)
    color_variant = models.CharField(max_length=100)
    ram_variant = models.TextField()
    memory = models.TextField()
    sim_type = models.CharField(max_length=50)
    battery = models.TextField()
    processor = models.TextField(max_length=50)
    front_camera = models.TextField()
    rear_camera = models.TextField()
    resolution = models.TextField()
    rating = models.IntegerField()
    highlights = models.TextField()

class laptop(models.Model):
    name = models.TextField(max_length=50)
    processor = models.TextField()
    ram = models.TextField()
    hdd = models.TextField()
    sdd = models.TextField()
    display = models.TextField()
    graphics = models.TextField()
    battery = models.TextField()
    rating = models.IntegerField()
    highlights = models.TextField()