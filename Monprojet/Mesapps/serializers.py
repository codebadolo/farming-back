from rest_framework import serializers
from .models import *

# Serializers entre les modèles Django et les formats JSON 

# -------------------- UTILISATEURS --------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class VendeurProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendeurProfile
        fields = '__all__'

class AcheteurProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcheteurProfile
        fields = '__all__'

# -------------------- PRODUITS --------------------

class ImageProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProduit
        fields = '__all__'

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class AttributSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributProduit
        fields = '__all__'

class ProduitSerializer(serializers.ModelSerializer):
    images = ImageProduitSerializer(many=True, read_only=True)
    class Meta:
        model = Produit
        fields = '__all__'

# -------------------- STOCK --------------------

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class MouvementStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouvementStock
        fields = '__all__'

# -------------------- COMMANDE --------------------

class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'

class ProduitCommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduitCommande
        fields = '__all__'
class ProduitMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ['id', 'nom', 'prix']

class ListeSouhaitSerializer(serializers.ModelSerializer):
    produit = ProduitMiniSerializer(read_only=True)
    produit_id = serializers.PrimaryKeyRelatedField(
        queryset=Produit.objects.all(),
        source='produit',
        write_only=True
    )
class Meta:
        model = ListeSouhait
        fields = ['id', 'utilisateur', 'produit', 'produit_id', 'date_ajout']
        read_only_fields = ['utilisateur', 'date_ajout']    
# -------------------- PROMOTION --------------------

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'

class ProduitPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduitPromotion
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class CouponCommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponCommande
        fields = '__all__'

# -------------------- LIVRAISON --------------------

class LivraisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livraison
        fields = '__all__'

# -------------------- PAIEMENT --------------------

class MethodePaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodePaiement
        fields = '__all__'

class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = '__all__'

# -------------------- PANIER --------------------

class PanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panier
        fields = '__all__'