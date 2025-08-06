from django.contrib import admin
from django.utils.html import format_html
from .models import Categorie, Produit, ImageProduit, AttributProduit, AvisProduit
from unfold.admin import ModelAdmin , TabularInline

class ImageProduitInline(TabularInline):
    """Inline pour les images des produits"""
    model = ImageProduit
    extra = 1
    fields = ('image', 'alt_text', 'ordre')


class AttributProduitInline(TabularInline):
    """Inline pour les attributs des produits"""
    model = AttributProduit
    extra = 1
    fields = ('nom_attribut', 'valeur')


@admin.register(Categorie)
class CategorieAdmin(ModelAdmin):
    """Administration des catégories"""
    
    list_display = ('nom', 'parent', 'niveau_display', 'active', 'ordre', 'date_creation')
    list_filter = ('active', 'parent', 'date_creation')
    search_fields = ('nom', 'description')
    prepopulated_fields = {'slug': ('nom',)}
    list_editable = ('active', 'ordre')
    ordering = ('ordre', 'nom')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'slug', 'description', 'parent')
        }),
        ('Affichage', {
            'fields': ('image', 'ordre', 'active')
        }),
    )
    
    def niveau_display(self, obj):
        return '—' * obj.niveau + f' Niveau {obj.niveau}'
    niveau_display.short_description = 'Niveau'


@admin.register(Produit)
class ProduitAdmin(ModelAdmin):
    """Administration des produits"""
    
    list_display = (
        'nom', 'vendeur', 'categorie', 'prix', 'status', 
        'featured', 'image_display', 'date_ajout'
    )
    list_filter = ('status', 'featured', 'categorie', 'date_ajout', 'vendeur')
    search_fields = ('nom', 'description', 'vendeur__username')
    prepopulated_fields = {'slug': ('nom',)}
    list_editable = ('status', 'featured', 'prix')
    readonly_fields = ('date_ajout', 'date_modification')
    inlines = [ImageProduitInline, AttributProduitInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'slug', 'description', 'categorie', 'vendeur')
        }),
        ('Prix et caractéristiques', {
            'fields': ('prix', 'poids', 'date_peremption')
        }),
        ('Publication', {
            'fields': ('status', 'featured')
        }),
        ('Dates', {
            'fields': ('date_ajout', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def image_display(self, obj):
        if obj.image_principale:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image_principale.image.url
            )
        return "Pas d'image"
    image_display.short_description = 'Image'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Les vendeurs ne voient que leurs produits
            if hasattr(request.user, 'role') and request.user.role == 'VENDEUR':
                qs = qs.filter(vendeur=request.user)
        return qs
    
    def save_model(self, request, obj, form, change):
        if not change:  # Nouveau produit
            if not request.user.is_superuser:
                obj.vendeur = request.user
        super().save_model(request, obj, form, change)


@admin.register(ImageProduit)
class ImageProduitAdmin(ModelAdmin):
    """Administration des images de produits"""
    
    list_display = ('produit', 'image_display', 'alt_text', 'ordre', 'date_ajout')
    list_filter = ('date_ajout',)
    search_fields = ('produit__nom', 'alt_text')
    list_editable = ('ordre',)
    
    def image_display(self, obj):
        return format_html(
            '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
            obj.image.url
        )
    image_display.short_description = 'Image'


@admin.register(AttributProduit)
class AttributProduitAdmin(ModelAdmin):
    """Administration des attributs de produits"""
    
    list_display = ('produit', 'nom_attribut', 'valeur', 'date_ajout')
    list_filter = ('nom_attribut', 'date_ajout')
    search_fields = ('produit__nom', 'nom_attribut', 'valeur')


@admin.register(AvisProduit)
class AvisProduitAdmin(ModelAdmin):
    """Administration des avis produits"""
    
    list_display = ('produit', 'utilisateur', 'note', 'modere', 'date_creation')
    list_filter = ('note', 'modere', 'date_creation')
    search_fields = ('produit__nom', 'utilisateur__username', 'commentaire')
    list_editable = ('modere',)
    readonly_fields = ('date_creation',)
    
    fieldsets = (
        ('Avis', {
            'fields': ('produit', 'utilisateur', 'note', 'commentaire')
        }),
        ('Modération', {
            'fields': ('modere', 'date_creation')
        }),
    )