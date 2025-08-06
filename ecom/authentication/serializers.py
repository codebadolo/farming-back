from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, VendeurProfile, AcheteurProfile


from django.utils.text import slugify

from django.utils.text import slugify
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, AcheteurProfile, VendeurProfile
import random


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], required=False)
    password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'nom', 'prenom', 'telephone',
            'role', 'status', 'date_inscription', 'password', 'password_confirm'
        )
        read_only_fields = ('id', 'date_inscription', 'status')

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if self.instance is None:
            # Création : password obligatoire et doit correspondre à password_confirm
            if not password:
                raise serializers.ValidationError({'password': 'Ce champ est obligatoire.'})
            if password != password_confirm:
                raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        else:
            # Mise à jour : si l'un des deux est fourni, vérifier qu'ils correspondent
            if (password or password_confirm) and password != password_confirm:
                raise serializers.ValidationError("Les mots de passe ne correspondent pas.")

        return attrs




    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')

        # Générer un username si pas fourni
        username = validated_data.get('username')
        if not username:
            email_username = validated_data['email'].split('@')[0]
            username = slugify(email_username)
            existing = CustomUser.objects.filter(username=username)
            if existing.exists():
                username += str(random.randint(100, 999))
            validated_data['username'] = username

        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        # Création automatique du profil selon le rôle
        if user.role == CustomUser.Role.CLIENT:
            AcheteurProfile.objects.create(utilisateur=user)
        elif user.role == CustomUser.Role.VENDEUR:
            VendeurProfile.objects.create(
                utilisateur=user,
                nom_entreprise=f"Entreprise de {user.nom_complet}",
                description="Description à compléter",
                adresse="Adresse à compléter",
                telephone_entreprise=user.telephone or ""
            )
        return user
    def update(self, instance, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance



class LoginSerializer(serializers.Serializer):
    """Serializer pour la connexion"""
    
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Email ou mot de passe incorrect.')
            if not user.is_active:
                raise serializers.ValidationError('Compte désactivé.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Email et mot de passe requis.')
        
        return attrs


class VendeurProfileSerializer(serializers.ModelSerializer):
    """Serializer pour les profils vendeurs"""
    
    utilisateur = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = VendeurProfile
        fields = '__all__'
        read_only_fields = ('date_creation', 'date_validation', 'status_validation')


class AcheteurProfileSerializer(serializers.ModelSerializer):
    """Serializer pour les profils acheteurs"""
    
    utilisateur = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = AcheteurProfile
        fields = '__all__'
        read_only_fields = ('date_creation',)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer pour changer le mot de passe"""
    
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer pour le profil utilisateur complet"""
    
    profil_vendeur = VendeurProfileSerializer(read_only=True)
    profil_acheteur = AcheteurProfileSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'nom', 'prenom', 'telephone',
            'role', 'status', 'date_inscription', 'profil_vendeur', 'profil_acheteur'
        )
        read_only_fields = ('id', 'username', 'role', 'status', 'date_inscription')