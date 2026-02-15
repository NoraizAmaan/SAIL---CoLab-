from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='chat_uploads/', blank=True, null=True)

    class Meta:
        ordering = ('timestamp',)

    @property
    def is_image(self):
        try:
            if self.file:
                image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
                return any(self.file.name.lower().endswith(ext) for ext in image_extensions)
        except:
            return False
        return False
