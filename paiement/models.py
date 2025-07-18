from django.db import models

# Mon modele paiement


class Paiement(models.Model):
    Statut_paiemnt = [
        ('en_attente', 'En attente'),
        ('effectue', 'Effectué'),
        ('ehec', 'Echec'), 
    ]
    utilisateur = models.ForeignKey('Utilisteur',on_delete=models.CASCADE)
    commande = models.OneToOneField('Commande',on_delete=models.CASCADE,related_name='paiement') # OneToOneField, une commande n'a qu'un seul paiement
    montant = models.DecimalField(max_digits=10,decimal_places=2)
    methode = models.CharField(max_length=50)
    statut = models.CharField(max_length=30,choices=Statut_paiemnt, default='en_attente')
    date_paiement = models.DateTimeField(auto_now_add=True)
    
def __str__(self):
    return f"Paiement #{self.id} - {self.utilisateur.email} - {self.statut}"

methode_paiement = [
    ('orange_money','Orange Money'),
    ('moov_money','Moov Money'),
    ('coris_money','Coris Money'),
    ('carte_bancaire','Carte Bancaire'),
]
methode = models.CharField(max_length=50,choices=methode_paiement)