from django.db import models

# Modele pour la notification

class Notification(models.Model):
    utilisateur = models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name='notification')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    
    def __str__(self) :
        return f"Notification pour {self.utilisateur.username} : {self.message[:30]}..."