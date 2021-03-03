from django.db import models

# Create your models here.


class UrlShortner(models.Model):
    slug = models.SlugField(max_length=255)
    url = models.URLField(max_length=2048)

    def __str__(self):
        return self.slug