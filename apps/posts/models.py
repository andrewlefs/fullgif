from django.db import models
from apps.core.models import Descriable, Timestampable
import uuid


# Create your models here.
class Post(Descriable, Timestampable):
    LANG = (
        (1, 'English'),
        (2, 'Vietnamese'),
    )
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, max_length=8)
    parent = models.TextField(max_length=255, blank=True, default='')
    image = models.TextField(blank=True, max_length=255, default='')
    webm = models.TextField(max_length=255, blank=True, default='')
    mp4 = models.TextField(max_length=255, blank=True, default='')
    lang = models.IntegerField(choices=LANG, default=1)

    class Meta:
        db_table = 'post'
