from django.db import models

# Mon modele produi


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    
    description = models.CharField(max_length=100)
    
    categorie = models.ForeignKey('Categorie', on_delete=models.SET_NULL, null=True)
    
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    
    poids = models.FloatField()
    
    peremption = models.DateField(null=True, blank=True)
    
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    image = models.ImageField(upload_to='produits/')
    
    vendeur = models.ForeignKey('Vendeur', on_delete=models.CASCADE)
    
def __str__(self):
    return self.nom

    
