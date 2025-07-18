from django.db import models

# Mon modele stock

class Stock (models.Model):
    produit = models.OneToOneField('produit',on_delete=models.CASCADE,related_name='stock')
    quantite=models.PositiveIntegerField(default=0)
def __str__(self):
    return f"Stock de {self.produit.nom}: {self.quantite}"

