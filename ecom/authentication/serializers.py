from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, VendeurProfile, AcheteurProfile


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer pour les utilisateurs"""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'nom', 'prenom', 'telephone', 
            'role', 'status', 'date_inscription', 'password', 'password_confirm'
        )
        read_only_fields = ('id', 'date_inscription', 'status')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Créer automatiquement le profil selon le rôle
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