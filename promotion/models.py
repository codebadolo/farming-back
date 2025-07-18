from django.db import models

# Le modele promotion

class Promotion(models.Model):
    nom = models.CharField(max_length=100)
    reduction = models.DecimalField(max_digits=5,decimal_places=2)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
def __str__(self):
    return f"{self.nom}({self.reduction}%)"

