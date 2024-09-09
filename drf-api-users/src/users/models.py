from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    avatar_url = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    is_2fa_enabled = models.BooleanField(default=False)
    id_42 = models.CharField(max_length=42)
    friends = models.ManyToManyField('self', blank=True)
    status = models.CharField(max_length=10, default='offline')
    in_game = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk or 'password' in kwargs.get('update_fields', []):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
    
    def add_friend(self, friend):
        if friend not in self.friends.all().values_list('id', flat=True):
            self.friends.add(friend)
            self.save()
            return True
        return False

    def remove_friend(self, friend):
        if friend in self.friends.all().values_list('id', flat=True):
            self.friends.remove(friend)
            self.save()
            return True
        return False