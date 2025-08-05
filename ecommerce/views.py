from django.shortcuts import render

from rest_framework import generics, status, permissions, viewsets
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.http import JsonResponse

# Les vues API du site

# Vue de l'API
def api_test(request):
    return JsonResponse({"message": "Hello from Django!"})

# Vues pour les produits
class ProduitListView(generics.ListCreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProduitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Vues pour les catégories
class CategorieListView(generics.ListCreateAPIView):
    queryset = Categorie.objects.filter(parent__isnull=True)  # Catégories principales
    serializer_class = CategorieSerializer
    permission_classes = [AllowAny]

class CategorieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

# La livraison
class LivraisonViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = LivraisonSerializer

class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer

# Vues pour les commandes
class CommandeListView(generics.ListCreateAPIView):
    serializer_class = CommandeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Commande.objects.filter(client__utilisateur=self.request.user)

class CommandeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommandeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Commande.objects.filter(client__utilisateur=self.request.user)

# Vues pour le panier
class PanierListView(generics.ListCreateAPIView):
    serializer_class = PanierSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        client = get_object_or_404(Client, utilisateur=self.request.user)
        return Panier.objects.filter(client=client)

# Vues pour les vendeurs
class VendeurListView(generics.ListAPIView):
    queryset = Vendeur.objects.filter(statut_validation='valide')
    serializer_class = VendeurSerializer
    permission_classes = [AllowAny]

class VendeurDetailView(generics.RetrieveUpdateAPIView):
    queryset = Vendeur.objects.all()
    serializer_class = VendeurSerializer
    permission_classes = [IsAuthenticated]

# API pour recherche de produits
@api_view(['GET'])
@permission_classes([AllowAny])
def rechercher_produits(request):
    query = request.GET.get('q', '')
    categorie = request.GET.get('categorie', '')
    prix_min = request.GET.get('prix_min', '')
    prix_max = request.GET.get('prix_max', '')
    
    produits = Produit.objects.all()
    
    if query:
        produits = produits.filter(nom__icontains=query)
    if categorie:
        produits = produits.filter(categorie__nom__icontains=categorie)
    if prix_min:
        produits = produits.filter(prix__gte=prix_min)
    if prix_max:
        produits = produits.filter(prix__lte=prix_max)
    
    serializer = ProduitSerializer(produits, many=True)
    return Response(serializer.data)
    return Response([])

@api_view(['POST'])
def initier_paiement_orange_money(request):
    """Initier un paiement Orange Money"""
    from .services import OrangeMoneyService
    
    try:
        commande_id = request.data.get('commande_id')
        numero_telephone = request.data.get('numero_telephone')
        
        if not commande_id or not numero_telephone:
            return Response({
                'error': 'commande_id et numero_telephone sont requis'
            }, status=400)
        
        commande = get_object_or_404(Commande, id=commande_id)
        
        # Vérifier que la commande n'est pas déjà payée
        if hasattr(commande, 'paiement'):
            return Response({
                'error': 'Cette commande a déjà un paiement associé'
            }, status=400)
        
        service = OrangeMoneyService()
        result = service.initier_paiement(commande, numero_telephone)
        
        if result['success']:
            return Response({
                'success': True,
                'transaction_id': result['transaction_id'],
                'payment_url': result['payment_url'],
                'message': result['message']
            })
        else:
            return Response({
                'success': False,
                'error': result['error']
            }, status=400)
            
    except Exception as e:
        return Response({
            'error': f'Erreur lors de l\'initiation du paiement: {str(e)}'
        }, status=500)

@api_view(['POST'])
def initier_paiement_carte_bancaire(request):
    """Initier un paiement par carte bancaire"""
    from .services import CarteBancaireService
    
    try:
        commande_id = request.data.get('commande_id')
        numero_carte = request.data.get('numero_carte')
        cvv = request.data.get('cvv')
        date_expiration = request.data.get('date_expiration')
        nom_porteur = request.data.get('nom_porteur')
        
        if not all([commande_id, numero_carte, cvv, date_expiration, nom_porteur]):
            return Response({
                'error': 'Tous les champs sont requis pour le paiement par carte'
            }, status=400)
        
        commande = get_object_or_404(Commande, id=commande_id)
        
        # Vérifier que la commande n'est pas déjà payée
        if hasattr(commande, 'paiement'):
            return Response({
                'error': 'Cette commande a déjà un paiement associé'
            }, status=400)
        
        service = CarteBancaireService()
        result = service.initier_paiement(
            commande, numero_carte, cvv, date_expiration, nom_porteur
        )
        
        if result['success']:
            return Response({
                'success': True,
                'transaction_id': result['transaction_id'],
                'authorization_code': result.get('authorization_code'),
                'message': result['message']
            })
        else:
            return Response({
                'success': False,
                'error': result['error']
            }, status=400)
            
    except Exception as e:
        return Response({
            'error': f'Erreur lors de l\'initiation du paiement: {str(e)}'
        }, status=500)

@api_view(['GET'])
def verifier_statut_paiement(request, transaction_id):
    """Vérifier le statut d'un paiement"""
    try:
        paiement = get_object_or_404(Paiement, reference_transac=transaction_id)
        
        data = {
            'transaction_id': transaction_id,
            'statut': paiement.statut,
            'montant': paiement.montant,
            'nom_methode': paiement.methode_paiement.nom_methode,
            'commande_id': paiement.commande.id
        }
        
        # Ajouter des détails spécifiques selon la méthode
        if paiement.methode_paiement.nom_methode == 'orange_money':
            try:
                orange_payment = paiement.methode_paiement.METHODES_CHOICES
                data['details_orange'] = {
                    'numero_telephone': PaiementOrangeMoney.numero_telephone,
                    'statut_orange': PaiementOrangeMoney.statut_orange,
                    'code_transaction': PaiementOrangeMoney.code_transaction
                }
            except:
                pass
        elif paiement.methode_paiement == 'carte_bancaire':
            try:
                carte_payment = paiement.methode_paiement.METHODES_CHOICES
                data['details_carte'] = {
                    'numero_carte_masque': PaiementCarteBancaire.numero_carte_masque,
                    'type_carte': PaiementCarteBancaire.type_carte,
                    'statut_banque': PaiementCarteBancaire.statut_banque,
                    'code_autorisation': PaiementCarteBancaire.code_autorisation
                }
            except:
                pass
        
        return Response(data)
        
    except Exception as e:
        return Response({
            'error': f'Erreur lors de la vérification: {str(e)}'
        }, status=500)

@api_view(['GET'])
def methodes_paiement_disponibles(request):
    """Obtenir la liste des méthodes de paiement disponibles"""
    pass

@api_view(['POST'])
def notification_orange_money(request):
    """Endpoint pour recevoir les notifications Orange Money"""
    try:
        # Traiter la notification (webhook)
        transaction_id = request.data.get('transaction_id')
        status = request.data.get('status')
        
        if transaction_id and status:
            try:
                paiement = Paiement.objects.get(reference_transac=transaction_id)
                orange_payment = PaiementOrangeMoney.objects.get(paiement=paiement)
                
                PaiementOrangeMoney.statut_orange = status
                PaiementOrangeMoney.date_traitement = datetime.now()
                orange_payment.save()
                
                # Mettre à jour le statut du paiement principal
                if status == 'success':
                    paiement.statut = 'complete'
                elif status == 'failed':
                    paiement.statut = 'echec'
                paiement.save()
                
                return Response({'status': 'ok'})
            except Paiement.DoesNotExist:
                return Response({'error': 'Paiement non trouvé'}, status=404)
        
        return Response({'error': 'Données manquantes'}, status=400)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)
