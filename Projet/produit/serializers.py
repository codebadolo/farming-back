from rest_framework import serializers
from .models import Categorie, Produit, Attribut, ListeSouhait

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = "__all__"

class AttributSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribut
        fields = "__all__"

class ProduitSerializer(serializers.ModelSerializer):
    attributs = AttributSerializer(many=True, read_only=True)

    class Meta:
        model = Produit
        fields = "__all__"

class ListeSouhaitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeSouhait
        fields = "__all__"