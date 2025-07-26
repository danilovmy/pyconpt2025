from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

class Pet(models.Model):
    STATUS_CHOICES = ( ('available', 'Available'), ('pending', 'Pending'), ('sold', 'Sold') )
    name = models.CharField(max_length=100)
    category = models.ForeignKey("Category", blank=True, null=True, on_delete=models.SET_NULL)
    photoUrls = models.URLField()
    tags = models.ManyToManyField(Tag, related_name="pets")
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, blank=True, null=True)
