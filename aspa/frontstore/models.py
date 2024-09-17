from django.db import models

# Create your models here.
from django.conf import settings
from aspamain.models import Industry, Category  # Import models from aspamain

class Store(models.Model):
    name = models.CharField(max_length=191)
    description = models.TextField()
    logo = models.ImageField(upload_to='store_logos/', null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stores')
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, related_name='stores')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='stores')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
