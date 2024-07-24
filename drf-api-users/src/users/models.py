from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    avatar_url = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    is_2fa_enabled = models.BooleanField(default=False)
    id_42 = models.CharField(max_length=42)
    friends = models.ManyToManyField('self', blank=True)

    def save(self, *args, **kwargs):
        if not self.pk or 'password' in kwargs.get('update_fields', []):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
