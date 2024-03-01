from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    category = models.OneToOneField(to=Category, on_delete=models.CASCADE, null=True, blank=True)
    preview_image = models.ImageField(upload_to='preview_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creation_timestamp = models.DateTimeField(auto_now_add=True)
