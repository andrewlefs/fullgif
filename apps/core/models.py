from django.db import models


# Create your models here.

class Descriable(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Timestampable(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
