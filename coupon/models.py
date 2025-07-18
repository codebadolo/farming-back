from django.db import models

# Le modele coupon

class Coupon(models.Model):
    code = models.CharField(max_length=50,unique=True)
    reduction = models.DecimalField(max_digits=10,decimal_places=2) # Reduction exprimée en pourcentage
    date_expiration = models.DateTimeField()
    
def __str__(self):
    return f"{self.code}(-{self.reduction}%)"
 
