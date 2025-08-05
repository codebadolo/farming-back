from rest_framework import serializers
from .models import *

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'identifiant', 'nom', 'prenom', 'email', 'telephone', 'role']
        extra_kwargs = {'password': {'write_only': True}}

class VendeurSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSerializer(read_only=True)
    
    class Meta:
        model = Vendeur
        fields = '__all__'

class CategorieSerializer(serializers.ModelSerializer):
    sous_categories = serializers.SerializerMethodField()
    
    class Meta:
        model = Categorie
        fields = ['id_categorie', 'nom', 'description', 'parent', 'sous_categories']
    
    def get_sous_categories(self, obj):
        return CategorieSerializer(obj.sous_categories.all(), many=True).data

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ProduitSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    vendeur = VendeurSerializer(read_only=True)
    categorie = CategorieSerializer(read_only=True)
    
    class Meta:
        model = Produit
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(read_only=True)
    
    class Meta:
        model = Stock
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    produits = serializers.SerializerMethodField()
    
    class Meta:
        model = Commande
        fields = '__all__'
    
    def get_produits(self, obj):
        return Product_CommandeSerializer(obj.produits.all(), many=True).data

class Product_CommandeSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(read_only=True) # This line is already correct.
    
    class Meta:
        model = Produit
        fields = '__all__'

class PanierSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(read_only=True)
    
    class Meta:
        model = Panier
        fields = '__all__'

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class LivraisonSerializer(serializers.ModelSerializer):
    commande = CommandeSerializer(read_only=True)
    
    class Meta:
        model = Stock
        fields = '__all__'
        
class PaiementSerializer(serializers.ModelSerializer):
    commande = CommandeSerializer(read_only=True)
    
    class Meta:
        model = Paiement
        fields = '__all__'



class MouvementStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouvementStock
        fields = '__all__'

class PaiementOrangeMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaiementOrangeMoney
        fields = '__all__'

class PaiementCarteBancaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaiementCarteBancaire
        fields = '__all__'

class InitierPaiementSerializer(serializers.Serializer):
    commande_id = serializers.IntegerField()
    methode_paiement = serializers.ChoiceField(choices=[
        ('orange_money', 'Orange Money'),
        ('carte_bancaire', 'Carte Bancaire')
    ])
    numero_telephone = serializers.CharField(max_length=15, required=False)
    numero_carte = serializers.CharField(max_length=20, required=False)
    cvv = serializers.CharField(max_length=4, required=False)
    date_expiration = serializers.CharField(max_length=7, required=False)  # MM/YYYY
    nom_porteur = serializers.CharField(max_length=100, required=False)
    
