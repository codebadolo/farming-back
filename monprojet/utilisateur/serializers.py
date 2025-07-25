from rest_framework import serializers
from .models import User, Adresse, Client, Vendeur

class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "telephone", "role", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(role=User.Role.CLIENT)
        client = Client.objects.create(user=user, **validated_data)
        return client


class VendeurSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Vendeur
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(role=User.Role.VENDEUR)
        vendeur = Vendeur.objects.create(user=user, **validated_data)
        return vendeur
    