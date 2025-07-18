from django.db import models
from .models import notification

# Mon modele livraison
class Livraison(models.Model):
    Statut_livraison = [
        ('en_attente','En attente'),
        ('expediee','Expediée'),
        ('livree','Livrée'),
        ('non_reussi','Non reussi'),
    ]
    commande = models.OneToOneField('Commande', on_delete=models.CASCADE,related_name='livraison') # OneToOneField exgige qu'il y ait une seule livraison par commande
    statut = models.CharField(max_length=20,choices=Statut_livraison,default='en_attente')
    date_expedition = models.DateTimeField(null=True,blank=True)
    date_livraison = models.DateTimeField(null=True, blank=True) 
    commentaire = models.TextField(blank=True,null=True)
    
def save(self, *args, **kwargs): # Mettre à jour automatiquement statut de livraison quand date_livraison sera renseigné
    is_new = self._state.adding 
    old = None
    if not is_new:
        old = Livraison.objects.get(pk=self.pk)
    if self.date_livraison and self.statut != 'livree': # Si on renseigne la date de livraison, statut devient 'livree'
     self.statut='livree'
        super().save(*args, **kwargs) # type: ignore 
        utilisateur = self.commande.utilisateur  # ignore sauvegarde réelle ici
        
    if old and old.date_expedition is None and self.date_expedition is not None: # Notification à l'expédition
        notification.objects.create( # type: ignore
            utilisateur = utilisateur,
            message = f"Votre commande #{self.commande.id} a été expédiée."
        )    
    if old and old.date_livraison is None and self.date_livraison is not None : # Notification à la livraison
        notification.objects.create( # type: ignore
            utilisateur = utilisateur,
            message = f"Votre commande #{self.commande.id} a été livrée avec succès."
        )   
def __str__(self):  
    return f"Livraison de la commande #{self.commande.id} - {self.statut}"