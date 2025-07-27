from django.db import models
from produit.models import Produit

# Mon modele pour les stocks
class Stock(models.Model):
    produit = models.OneToOneField(Produit, on_delete=models.CASCADE, related_name="stock")
    qte_disponible = models.PositiveIntegerField(default=0)
    seuil_alerte = models.PositiveIntegerField(default=0)
    date_maj = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stock {self.produit} : {self.qte_disponible}"

class MouvementStock(models.Model):
    class Type(models.TextChoices):
        ENTREE = "IN", "Entrée"
        SORTIE = "OUT", "Sortie"
    type = models.CharField(max_length=3, choices=Type.choices)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="mouvements")
    qte = models.PositiveIntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.type} {self.qte} {self.produit}"