from django.contrib import admin
from .models import Stock, MouvementStock, AlerteStock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'quantite_disponible', 'seuil_alerte', 'en_rupture', 'alerte_stock', 'date_mise_a_jour')
    list_filter = ('date_mise_a_jour',)
    search_fields = ('produit__nom',)
    readonly_fields = ('date_mise_a_jour',)


@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'type_mouvement', 'quantite', 'date_mouvement', 'utilisateur')
    list_filter = ('type_mouvement', 'date_mouvement')
    search_fields = ('produit__nom', 'commentaire')
    readonly_fields = ('date_mouvement',)


@admin.register(AlerteStock)
class AlerteStockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'type_alerte', 'status', 'date_creation')
    list_filter = ('type_alerte', 'status', 'date_creation')
    search_fields = ('produit__nom', 'message')
    readonly_fields = ('date_creation', 'date_resolution')