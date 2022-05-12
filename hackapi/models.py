from django.db import models

# Create your models here.


class NameModel(models.Model):
    name_text = models.CharField(max_length=100)
    audio_file = models.TextField()

    def __str__(self):
        return self.name_text
