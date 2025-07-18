from django.db import models

# Le modele liste de souhait

class Listesouhait(models.Model):
    utilisateur = models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name='liste_souhait')
    produit = models.ForeignKey('Produit',on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)
class Meta:
    unique_together = ('utilisateur','produit')
def __str__(self):
    return f"{self.utilisateur.username} souhaite {self.produit.nom}"

