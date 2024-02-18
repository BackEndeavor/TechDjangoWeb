from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='preview_images/')
    price = models.DecimalField()
    creation_timestamp = models.DateTimeField(auto_now_add=True)
