from django.db import models


class Video(models.Model):
    name = models.CharField(max_length=100,default=1)
    video_file = models.FileField(upload_to='Videos/', null=True)

    
    def __str__(self):
        return self.name