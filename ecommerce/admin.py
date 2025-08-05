from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('email', 'nom', 'prenom', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('email', 'nom', 'prenom')
    ordering = ('email',)
    
    fieldsets = list(UserAdmin.fieldsets) + [
    ("Informations", {
        'fields': ('nom', 'prenom', 'telephone', 'role',)
    }),
]

admin.register(Vendeur)

@admin.register(Vendeur)
class VendeurAdmin(admin.ModelAdmin):
    list_display = ('entreprise', 'utilisateur', 'statut_validation')
    list_filter = ('statut_validation',)
    search_fields = ('entreprise', 'utilisateur__email')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'localisation')
    search_fields = ('utilisateur__email', 'utilisateur__nom')

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'parent')
    list_filter = ('parent',)
    search_fields = ('nom',)

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix', 'vendeur', 'date_ajout')
    list_filter = ('categorie', 'date_ajout', 'vendeur')
    search_fields = ('nom', 'description')
    inlines = [ImageInline]
    

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'qte_disponible', 'seuil_alerte', 'date_maj')
    list_filter = ('date_maj',)
    search_fields = ('produit__nom',)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'statut', 'montant_total', 'date_creation']  # Noms de champs valides
    list_filter = ['statut', 'date_creation']  # Champs existants

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_promotion', 'valeur', 'date_debut', 'date_fin', 'statut')
    list_filter = ('type_promotion', 'statut', 'date_debut')
    search_fields = ('nom',)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'type', 'valeur', 'debut', 'fin', 'statut')
    list_filter = ('type', 'statut', 'debut')
    search_fields = ('code',)

# Enregistrer les autres modèles
admin.site.register(Adresse)
admin.site.register(Image)
admin.site.register(Attribut)
admin.site.register(Panier)
admin.site.register(Produit_Commande)
admin.site.register(Methode_Paiement)
admin.site.register(Liste_Souhait)
admin.site.register(MouvementStock)
admin.site.register(Produit_Promo)
admin.site.register(CouponCommande)
