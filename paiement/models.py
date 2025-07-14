from django.db import models

# Mon modele paiement


class Paiement(models.Model):
    Statut_choix = [
        ('en_attente', 'En attente'),
        ('effectue', 'Effectué'),
        ('ehec', 'Echec'), 
    ]
    reference_transaction = models.CharField(max_length=100, unique=True)
    
    methode = models.ForeignKey('MethodePaiement', on_delete=models.SET_NULL, null=True)
    
    montant = models.DecimalField(max_digits=10,decimal_places=2)
    
    commande = models.ForeignKey('Commande', on_delete=models.CASCADE)
    
    statut = models.CharField(max_length=30,choices=Statut_choix, default='en attente')
    
    def __str__(self):
        return f"{self.reference_transaction} - {self.statut}"