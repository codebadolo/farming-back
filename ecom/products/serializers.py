from rest_framework import serializers
from .models import Categorie, Produit, ImageProduit, AttributProduit, AvisProduit


class CategorieSerializer(serializers.ModelSerializer):
    """Serializer pour les catégories"""
    
    sous_categories = serializers.SerializerMethodField()
    niveau = serializers.ReadOnlyField()
    
    class Meta:
        model = Categorie
        fields = '__all__'
        read_only_fields = ('slug', 'date_creation')
    
    def get_sous_categories(self, obj):
        if obj.sous_categories.exists():
            return CategorieSerializer(obj.sous_categories.all(), many=True).data
        return []


class ImageProduitSerializer(serializers.ModelSerializer):
    """Serializer pour les images de produits"""
    
    class Meta:
        model = ImageProduit
        fields = '__all__'
        read_only_fields = ('date_ajout',)


class AttributProduitSerializer(serializers.ModelSerializer):
    """Serializer pour les attributs de produits"""
    
    class Meta:
        model = AttributProduit
        fields = '__all__'
        read_only_fields = ('date_ajout',)


class AvisProduitSerializer(serializers.ModelSerializer):
    """Serializer pour les avis produits"""
    
    utilisateur_nom = serializers.CharField(source='utilisateur.username', read_only=True)
    
    class Meta:
        model = AvisProduit
        fields = '__all__'
        read_only_fields = ('date_creation', 'modere')
    
    def create(self, validated_data):
        validated_data['utilisateur'] = self.context['request'].user
        return super().create(validated_data)


class ProduitListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des produits (version allégée)"""
    
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    vendeur_nom = serializers.CharField(source='vendeur.username', read_only=True)
    image_principale = serializers.SerializerMethodField()
    prix_avec_promotion = serializers.ReadOnlyField()
    note_moyenne = serializers.SerializerMethodField()
    
    class Meta:
        model = Produit
        fields = [
            'id', 'nom', 'slug', 'prix', 'prix_avec_promotion', 
            'categorie_nom', 'vendeur_nom', 'image_principale',
            'status', 'featured', 'note_moyenne', 'date_ajout'
        ]
    
    def get_image_principale(self, obj):
        if obj.image_principale:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_principale.image.url)
        return None
    
    def get_note_moyenne(self, obj):
        avis = obj.avis.filter(modere=True)
        if avis.exists():
            return round(sum(avis.values_list('note', flat=True)) / avis.count(), 1)
        return 0


class ProduitDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour un produit"""
    
    categorie = CategorieSerializer(read_only=True)
    categorie_id = serializers.IntegerField(write_only=True)
    vendeur_nom = serializers.CharField(source='vendeur.username', read_only=True)
    images = ImageProduitSerializer(many=True, read_only=True)
    attributs = AttributProduitSerializer(many=True, read_only=True)
    avis = serializers.SerializerMethodField()
    prix_avec_promotion = serializers.ReadOnlyField()
    note_moyenne = serializers.SerializerMethodField()
    nombre_avis = serializers.SerializerMethodField()
    stock_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Produit
        fields = '__all__'
        read_only_fields = ('slug', 'date_ajout', 'date_modification', 'vendeur')
    
    def get_avis(self, obj):
        avis_moderes = obj.avis.filter(modere=True).order_by('-date_creation')[:5]
        return AvisProduitSerializer(avis_moderes, many=True).data
    
    def get_note_moyenne(self, obj):
        avis = obj.avis.filter(modere=True)
        if avis.exists():
            return round(sum(avis.values_list('note', flat=True)) / avis.count(), 1)
        return 0
    
    def get_nombre_avis(self, obj):
        return obj.avis.filter(modere=True).count()
    
    def get_stock_info(self, obj):
        try:
            from stock.models import Stock
            stock = Stock.objects.get(produit=obj)
            return {
                'quantite_disponible': stock.quantite_disponible,
                'seuil_alerte': stock.seuil_alerte,
                'en_stock': stock.quantite_disponible > 0
            }
        except:
            return {
                'quantite_disponible': 0,
                'seuil_alerte': 0,
                'en_stock': False
            }
    
    def create(self, validated_data):
        validated_data['vendeur'] = self.context['request'].user
        return super().create(validated_data)


class ProduitCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour créer/modifier un produit"""
    
    images_data = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    attributs_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Produit
        fields = '__all__'
        read_only_fields = ('slug', 'date_ajout', 'date_modification', 'vendeur')
    
    def create(self, validated_data):
        images_data = validated_data.pop('images_data', [])
        attributs_data = validated_data.pop('attributs_data', [])
        validated_data['vendeur'] = self.context['request'].user
        
        produit = Produit.objects.create(**validated_data)
        
        # Créer les images
        for i, image_data in enumerate(images_data):
            ImageProduit.objects.create(
                produit=produit,
                image=image_data,
                ordre=i
            )
        
        # Créer les attributs
        for attribut_data in attributs_data:
            AttributProduit.objects.create(
                produit=produit,
                **attribut_data
            )
        
        return produit
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images_data', None)
        attributs_data = validated_data.pop('attributs_data', None)
        
        # Mettre à jour le produit
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Mettre à jour les images si fournies
        if images_data is not None:
            instance.images.all().delete()
            for i, image_data in enumerate(images_data):
                ImageProduit.objects.create(
                    produit=instance,
                    image=image_data,
                    ordre=i
                )
        
        # Mettre à jour les attributs si fournis
        if attributs_data is not None:
            instance.attributs.all().delete()
            for attribut_data in attributs_data:
                AttributProduit.objects.create(
                    produit=instance,
                    **attribut_data
                )
        
        return instance


class CategorieTreeSerializer(serializers.ModelSerializer):
    """Serializer pour l'arbre des catégories"""
    
    children = serializers.SerializerMethodField()
    produits_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Categorie
        fields = ['id', 'nom', 'slug', 'description', 'image', 'children', 'produits_count']
    
    def get_children(self, obj):
        if obj.sous_categories.filter(active=True).exists():
            return CategorieTreeSerializer(
                obj.sous_categories.filter(active=True), 
                many=True, 
                context=self.context
            ).data
        return []
    
    def get_produits_count(self, obj):
        return obj.produits.filter(status='PUBLIE').count()