from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from .models import CustomUser, VendeurProfile, AcheteurProfile
from .serializers import (
    CustomUserSerializer, LoginSerializer, VendeurProfileSerializer,
    AcheteurProfileSerializer, ChangePasswordSerializer, UserProfileSerializer
)


class RegisterView(generics.CreateAPIView):
    """Vue pour l'inscription des utilisateurs"""
    
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Créer le token d'authentification
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': CustomUserSerializer(user).data,
            'token': token.key,
            'message': 'Inscription réussie'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Vue pour la connexion"""
    
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        # Créer ou récupérer le token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'Connexion réussie'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Vue pour la déconnexion"""
    
    try:
        # Supprimer le token
        request.user.auth_token.delete()
    except:
        pass
    
    logout(request)
    return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """Vue pour consulter et modifier le profil utilisateur"""
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class VendeurProfileView(generics.RetrieveUpdateAPIView):
    """Vue pour le profil vendeur"""
    
    serializer_class = VendeurProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role != CustomUser.Role.VENDEUR:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Accès réservé aux vendeurs')
        
        profile, created = VendeurProfile.objects.get_or_create(
            utilisateur=user,
            defaults={
                'nom_entreprise': f"Entreprise de {user.nom_complet}" if hasattr(user, 'nom_complet') else f"Entreprise de {user.username}",
                'description': "Description à compléter",
                'adresse': "Adresse à compléter",
                'telephone_entreprise': getattr(user, 'telephone', '') or ""
            }
        )
        return profile


class AcheteurProfileView(generics.RetrieveUpdateAPIView):
    """Vue pour le profil acheteur"""
    
    serializer_class = AcheteurProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        if hasattr(user, 'role') and user.role != CustomUser.Role.CLIENT:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Accès réservé aux clients')
        
        profile, created = AcheteurProfile.objects.get_or_create(utilisateur=user)
        return profile


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    """Vue pour changer le mot de passe"""
    
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Régénérer le token
        try:
            user.auth_token.delete()
        except:
            pass
        token = Token.objects.create(user=user)
        
        return Response({
            'message': 'Mot de passe modifié avec succès',
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendeurListView(generics.ListAPIView):
    """Vue pour lister les vendeurs validés"""
    
    serializer_class = VendeurProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return VendeurProfile.objects.filter(
            status_validation=VendeurProfile.StatusValidation.VALIDE
        ).select_related('utilisateur')


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def vendeur_detail_view(request, vendeur_id):
    """Vue pour les détails d'un vendeur"""
    
    vendeur = get_object_or_404(
        VendeurProfile, 
        id=vendeur_id,
        status_validation=VendeurProfile.StatusValidation.VALIDE
    )
    
    serializer = VendeurProfileSerializer(vendeur)
    return Response(serializer.data, status=status.HTTP_200_OK)