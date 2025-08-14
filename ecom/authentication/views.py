from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import generics, status, filters, permissions
from rest_framework.decorators import api_view, permission_classes, action ,authentication_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from .models import CustomUser, VendeurProfile, AcheteurProfile
from .serializers import (
    CustomUserSerializer, LoginSerializer, VendeurProfileSerializer,
    AcheteurProfileSerializer, ChangePasswordSerializer, UserProfileSerializer
)
from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny
class RegisterView(generics.CreateAPIView):
    """Vue pour l'inscription des utilisateurs"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'user': CustomUserSerializer(user).data,
            'token': token.key,
            'message': 'Inscription réussie'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([])   
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Vue pour la connexion"""

    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)

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
        request.user.auth_token.delete()
    except Exception:
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
        if user.role != CustomUser.Role.VENDEUR:
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
        if user.role != CustomUser.Role.CLIENT:
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

        try:
            user.auth_token.delete()
        except Exception:
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


# Additional user management APIs for admin:

class UserListView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all().order_by('-date_inscription')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'status']
    search_fields = ['nom', 'prenom', 'email', 'username']
    ordering_fields = ['date_inscription', 'nom']


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def update_user_status(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    status_value = request.data.get('status')
    if status_value not in CustomUser.Status.values:
        return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    user.status = status_value
    user.save()
    serializer = CustomUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class AdminResetPasswordView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'detail': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(new_password)
        except Exception as e:
            return Response({'detail': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password updated successfully'}, status=status.HTTP_200_OK)


class VendeurProfileAdminViewSet(ModelViewSet):
    queryset = VendeurProfile.objects.all()
    serializer_class = VendeurProfileSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def validate(self, request, pk=None):
        profile = self.get_object()
        status_val = request.data.get('status_validation')
        if status_val not in VendeurProfile.StatusValidation.values:
            return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        profile.status_validation = status_val
        if status_val == VendeurProfile.StatusValidation.VALIDE:
            profile.date_validation = timezone.now()
        else:
            profile.date_validation = None
        profile.save()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
