from django.db import models


# TODO: remove blank using patch instead put to update data
class User(models.Model):
    username = models.CharField(max_length=100, blank=True)
    avatar_url = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=128, blank=True)
    is_2fa_enabled = models.BooleanField(default=False)
    id_42 = models.CharField(max_length=42, blank=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.username
