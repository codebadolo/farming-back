from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from .permissions import IsAdminUser, IsVendeurUser, IsClientUser, IsOwnerOrAdmin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Produit, Panier, ListeSouhait,PanierItem

# Les différentes vues de mon application pour la gestion de la logique CRUD

# === Utilisateurs, Profils ===
class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class VendeurProfileViewSet(viewsets.ModelViewSet):
    queryset = VendeurProfile.objects.all()
    serializer_class = VendeurProfileSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsVendeurUser()]
        return [permissions.AllowAny()]

class AcheteurProfileViewSet(viewsets.ModelViewSet):
    queryset = AcheteurProfile.objects.all()
    serializer_class = AcheteurProfileSerializer
    permission_classes = [IsClientUser]

# === Produits ===
class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsVendeurUser()]
        return [permissions.AllowAny()]

class ProduitImageViewSet(viewsets.ModelViewSet):
    queryset = ImageProduit.objects.all()
    serializer_class = ImageProduitSerializer
    permission_classes = [IsVendeurUser]

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [permissions.AllowAny]

class AttributViewSet(viewsets.ModelViewSet):
    queryset = AttributProduit.objects.all()
    serializer_class = AttributSerializer
    permission_classes = [IsVendeurUser]

# === Stock ===
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsVendeurUser]

class MouvementStockViewSet(viewsets.ModelViewSet):
    queryset = MouvementStock.objects.all()
    serializer_class = MouvementStockSerializer
    permission_classes = [IsVendeurUser]

# === Commande ===
class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsClientUser()]
        elif self.action in ['list', 'retrieve']:
            return [IsOwnerOrAdmin()]
        return [IsAdminUser()]

class ProduitCommandeViewSet(viewsets.ModelViewSet):
    queryset = ProduitCommande.objects.all()
    serializer_class = ProduitCommandeSerializer
    permission_classes = [IsAdminUser]

# === Promotions ===
class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAdminUser]

class ProduitPromotionViewSet(viewsets.ModelViewSet):
    queryset = ProduitPromotion.objects.all()
    serializer_class = ProduitPromotionSerializer
    permission_classes = [IsAdminUser]

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]

class CouponCommandeViewSet(viewsets.ModelViewSet):
    queryset = CouponCommande.objects.all()
    serializer_class = CouponCommandeSerializer
    permission_classes = [IsAdminUser]

# === Livraison ===
class AdresseViewSet(viewsets.ModelViewSet):
    queryset = Adresse.objects.all()
    serializer_class = AdresseSerializer
    permission_classes = [IsClientUser]

class LivraisonViewSet(viewsets.ModelViewSet):
    queryset = Livraison.objects.all()
    serializer_class = LivraisonSerializer
    permission_classes = [IsAdminUser]

# === Paiement ===
class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer
    permission_classes = [IsClientUser]

class MethodePaiementViewSet(viewsets.ModelViewSet):
    queryset = MethodePaiement.objects.all()
    serializer_class = MethodePaiementSerializer
    permission_classes = [IsAdminUser]

# === Panier ===
class PanierViewSet(viewsets.ModelViewSet):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer
    permission_classes = [IsClientUser]
    
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest  # Optionnel, pour autocomplétion
from .models import Produit, Categorie

def home(request):
    produits = Produit.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'home.html', {
        'produits': produits,
        'categories': categories
    })
    
def produit_detail(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    return render(request, 'produit_detail.html', {'produit': produit})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Panier, PanierItem

@login_required
def modify_panier(request):
    panier_items = PanierItem.objects.filter(panier__utilisateur=request.user)

    if request.method == "POST":
        for item in panier_items:
            field_name = 'quantite_' + str(item.id)  # type: ignore
            new_quantite = request.POST.get(field_name)

            if new_quantite:
                try:
                    item.quantite = int(new_quantite)
                    item.save()
                except ValueError:
                    pass

        return redirect('voir_panier')

    return render(request, 'modify_panier.html', {'panier_items': panier_items})

@login_required
def delete_produit_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    panier = get_object_or_404(Panier, utilisateur=request.user, produit=produit)
    if request.method == "POST":
        panier.delete()
        return redirect('voir_panier')
    return render(request, 'delete_produit_panier.html', {'produit': produit})

@login_required
def ajouter_liste_souhait(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    souhait, created = ListeSouhait.objects.get_or_create(utilisateur=request.user, produit=produit)
    return render(request, 'add_listesouhait.html', {'produit': produit})

def boutique(request):
    produits = Produit.objects.all().prefetch_related('images', 'vendeur')
    return render(request, 'boutique.html', {'produits': produits})
@login_required
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    quantite = int(request.POST.get('quantite', 1))

    panier_item, created = Panier.objects.get_or_create(
        utilisateur=request.user,
        produit=produit,
        defaults={'quantite': quantite}
    )

    if not created:
        panier_item.quantite += quantite
        panier_item.save()
    return redirect('voir_panier')  # nom de la route vers le panier

@login_required
def update_panier(request):
    if request.method == 'POST':
        panier_items = Panier.objects.filter(utilisateur=request.user)
        for item in panier_items:
            field_name = f'quantite_{item.id}' # type: ignore
            new_quantite = request.POST.get(field_name)
            if new_quantite:
                try:
                    item.quantite = int(new_quantite)
                    item.save()
                except ValueError:
                    continue  # ignore les valeurs invalides
        return redirect('voir_panier')

    panier_items = Panier.objects.filter(utilisateur=request.user)
    return render(request, 'update_panier.html', {'panier': panier_items})
