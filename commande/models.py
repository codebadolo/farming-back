from django.db import models

# Mon modele commande

class commande(models.Model):
    utilisateur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=60,
                              choices=[
                                  ('en_attent','En attente'),
                                  ('en_cours','En cours'),
                                  ('livree','Livrée')
                              ])
    adresse_livraison = models.TextField()
    
    def __str__(self):
        return f"commande #{self.id} - {self.utilisateur.email}" # type: ignore
    def get_total_commande(self):
        return sum([cp.get_total()
    for cp in 
    self.commande_produits.all]) # type: ignore
    
