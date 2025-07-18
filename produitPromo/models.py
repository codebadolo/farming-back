from django.db import models

# Mon modele produit promo

class Produitpromo(models.Model):
    produit = models.ForeignKey('Produit',on_delete=models.CASCADE)
    promotion = models.ForeignKey('Promotion',on_delete=models.CASCADE)
def __str__(self):
    return f"{self.produit.nom} ´n {self.promotion.nom}"

