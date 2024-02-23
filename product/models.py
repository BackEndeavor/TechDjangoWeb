from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=64)
    preview_image = models.ImageField(upload_to='preview_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creation_timestamp = models.DateTimeField(auto_now_add=True)
