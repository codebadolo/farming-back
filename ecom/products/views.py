from rest_framework import generics, filters, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg
from .models import Categorie, Produit, ImageProduit, AttributProduit, AvisProduit
from .serializers import (
    CategorieSerializer, CategorieTreeSerializer, ProduitListSerializer,
    ProduitDetailSerializer, ProduitCreateUpdateSerializer, AvisProduitSerializer,
    ImageProduitSerializer, AttributProduitSerializer
)


class CategorieListView(generics.ListCreateAPIView):
    """Vue pour lister et créer les catégories"""
    
    queryset = Categorie.objects.filter(active=True).order_by('ordre', 'nom')
    serializer_class = CategorieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'description']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        parent_id = self.request.query_params.get('parent', None)
        
        if parent_id is not None:
            if parent_id == '0':  # Catégories racines
                queryset = queryset.filter(parent=None)
            else:
                queryset = queryset.filter(parent_id=parent_id)
        
        return queryset


class CategorieDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour les détails d'une catégorie"""
    
    queryset = Categorie.objects.filter(active=True)
    serializer_class = CategorieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def categories_tree_view(request):
    """Vue pour l'arbre complet des catégories"""
    
    categories_racines = Categorie.objects.filter(
        parent=None, 
        active=True
    ).order_by('ordre', 'nom')
    
    serializer = CategorieTreeSerializer(
        categories_racines, 
        many=True, 
        context={'request': request}
    )
    
    return Response(serializer.data)


class ProduitListView(generics.ListAPIView):
    """Vue pour lister les produits"""
    
    serializer_class = ProduitListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categorie', 'vendeur', 'status', 'featured']
    search_fields = ['nom', 'description']
    ordering_fields = ['prix', 'date_ajout', 'nom']
    ordering = ['-date_ajout']
    
    def get_queryset(self):
        queryset = Produit.objects.filter(status='PUBLIE').select_related(
            'categorie', 'vendeur'
        ).prefetch_related('images', 'avis')
        
        # Filtres personnalisés
        prix_min = self.request.query_params.get('prix_min')
        prix_max = self.request.query_params.get('prix_max')
        categorie_slug = self.request.query_params.get('categorie_slug')
        vendeur_id = self.request.query_params.get('vendeur_id')
        featured = self.request.query_params.get('featured')
        
        if prix_min:
            queryset = queryset.filter(prix__gte=prix_min)
        if prix_max:
            queryset = queryset.filter(prix__lte=prix_max)
        if categorie_slug:
            queryset = queryset.filter(categorie__slug=categorie_slug)
        if vendeur_id:
            queryset = queryset.filter(vendeur_id=vendeur_id)
        if featured:
            queryset = queryset.filter(featured=True)
        
        return queryset


class ProduitDetailView(generics.RetrieveAPIView):
    """Vue pour les détails d'un produit"""
    
    queryset = Produit.objects.filter(status='PUBLIE')
    serializer_class = ProduitDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class ProduitCreateView(generics.CreateAPIView):
    """Vue pour créer un produit"""
    
    serializer_class = ProduitCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Vérifier que l'utilisateur est un vendeur
        user = self.request.user
        if not hasattr(user, 'role') or user.role != 'VENDEUR':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Seuls les vendeurs peuvent créer des produits")
        
        serializer.save(vendeur=user)


class ProduitUpdateView(generics.UpdateAPIView):
    """Vue pour modifier un produit"""
    
    serializer_class = ProduitCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Produit.objects.all()
        return Produit.objects.filter(vendeur=user)


class ProduitDeleteView(generics.DestroyAPIView):
    """Vue pour supprimer un produit"""
    
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Produit.objects.all()
        return Produit.objects.filter(vendeur=user)


class MesProduitsView(generics.ListAPIView):
    """Vue pour les produits du vendeur connecté"""
    
    serializer_class = ProduitListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'description']
    ordering_fields = ['prix', 'date_ajout', 'nom', 'status']
    ordering = ['-date_ajout']
    
    def get_queryset(self):
        return Produit.objects.filter(vendeur=self.request.user).select_related('categorie').prefetch_related('images', 'avis')


class AvisProduitListCreateView(generics.ListCreateAPIView):
    """Vue pour lister et créer des avis sur un produit"""
    
    serializer_class = AvisProduitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        produit_id = self.kwargs['produit_id']
        return AvisProduit.objects.filter(
            produit_id=produit_id,
            modere=True
        ).order_by('-date_creation')
    
    def perform_create(self, serializer):
        produit_id = self.kwargs['produit_id']
        
        # Vérifier que l'utilisateur n'a pas déjà donné un avis
        if AvisProduit.objects.filter(
            produit_id=produit_id,
            utilisateur=self.request.user
        ).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Vous avez déjà donné un avis sur ce produit")
        
        serializer.save(produit_id=produit_id, utilisateur=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def produits_featured_view(request):
    """Vue pour les produits mis en avant"""
    
    produits = Produit.objects.filter(
        status='PUBLIE',
        featured=True
    ).select_related('categorie', 'vendeur').prefetch_related('images')[:8]
    
    serializer = ProduitListSerializer(
        produits, 
        many=True, 
        context={'request': request}
    )
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def produits_similaires_view(request, produit_id):
    """Vue pour les produits similaires"""
    
    try:
        produit = Produit.objects.get(id=produit_id, status='PUBLIE')
        
        produits_similaires = Produit.objects.filter(
            categorie=produit.categorie,
            status='PUBLIE'
        ).exclude(id=produit_id).select_related(
            'categorie', 'vendeur'
        ).prefetch_related('images')[:6]
        
        serializer = ProduitListSerializer(
            produits_similaires, 
            many=True, 
            context={'request': request}
        )
        
        return Response(serializer.data)
        
    except Produit.DoesNotExist:
        return Response(
            {'error': 'Produit non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_image_produit_view(request, produit_id):
    """Vue pour uploader une image de produit"""
    
    try:
        produit = Produit.objects.get(id=produit_id, vendeur=request.user)
        
        serializer = ImageProduitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(produit=produit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Produit.DoesNotExist:
        return Response(
            {'error': 'Produit non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_attribut_produit_view(request, produit_id):
    """Vue pour ajouter un attribut à un produit"""
    
    try:
        produit = Produit.objects.get(id=produit_id, vendeur=request.user)
        
        serializer = AttributProduitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(produit=produit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Produit.DoesNotExist:
        return Response(
            {'error': 'Produit non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )