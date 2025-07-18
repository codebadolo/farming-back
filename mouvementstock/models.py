from django.db import models

# Modele mouvement stock

class Mouvementstock = (models.Model):
    Type_mouvement = [
        ('entree','Entrée'),
        ('sortie','Sortie'),
    ]
    produit = models.ForeignKey('Produit',on_delete=models.CASCADE)
    type_mouvement = models.CharField(max_length=10, choices=Type_mouvement)
    quantite = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True,null=True)
def __str__(self):
    return f"{self.type_mouvement} - {self.produit.nom} ({self.quantite})"

