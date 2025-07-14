from django.db import models

# Mon modele commande

class commande(models.Model):
    Statut_choix = [
        ('en_attente','En attente'),
        ('validee', 'Validée'),
        ('annulee', 'Annulée'),
        ('livree', 'Livrée'),
    ]
    
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    
    date_commande = models.DateTimeField(auto_now_add=True)
    
    statut = models.CharField(max_length=30, choices=Statut_choix, default='en_attente')
    
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    adresse_livraison = models.ForeignKey('Adresse', on_delete=models.SET_NULL, null = True)
    
    date_livraison = models.DateField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f"commande {self.id} - {self.client}" # type: ignore
