from django.db import models

class Game(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]
    player1_id = models.IntegerField(null=True, blank=True)
    player2_id = models.IntegerField(null=True, blank=True)
    player1_name = models.CharField(max_length=20, null=True, blank=True)
    player2_name = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    winner_id = models.IntegerField(null=True, blank=True)
    loser_id = models.IntegerField(null=True, blank=True)
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    tournament_id = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=True) 

class Tournament(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    games = models.ManyToManyField(Game)

