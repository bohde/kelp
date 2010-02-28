from django.db import models

class ProgrammingAudio(models.Model):
    short_name = models.SlugField()
    date = models.DateField()
    title = models.CharField(max_length=200, unique=True)
    length = models.CharField(max_length=20)
    audio_file = models.URLField()
    description = models.TextField()
    
    @staticmethod
    def get_feed(slug):
        return ProgrammingAudio.objects.filter(short_name=slug)
    
    
