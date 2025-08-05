import requests
import json
import uuid
from datetime import datetime, timedelta
from django.conf import settings
from .models import *

class OrangeMoneyService:
    def __init__(self):
        self.api_url = "https://api.orange.com/orange-money-webpay/dev/v1"
        self.merchant_key = getattr(settings, 'ORANGE_MONEY_MERCHANT_KEY', 'demo_key')
        self.client_id = getattr(settings, 'ORANGE_MONEY_CLIENT_ID', 'demo_client')
        self.client_secret = getattr(settings, 'ORANGE_MONEY_CLIENT_SECRET', 'demo_secret')

    def get_access_token(self):
        """Obtenir un token d'accès Orange Money"""
        try:
            # En mode démo, retourner un token fictif
            return "demo_access_token_12345"
        except Exception as e:
            raise Exception(f"Erreur lors de l'obtention du token: {str(e)}")

    def initier_paiement(self, commande, numero_telephone):
        """Initier un paiement Orange Money"""
        try:
            # Générer un ID de transaction unique
            transaction_id = f"TXN_{uuid.uuid4().hex[:10].upper()}"
            
            # Données de la requête (format démo)
            payment_data = {
                "merchant_key": self.merchant_key,
                "currency": "XOF",
                "order_id": commande.id,
                "amount": int(float(commande.montant_total) * 100),  # Convertir en centimes
                "description": f"Commande #{commande.id}",
                "return_url": f"{settings.SITE_URL}/paiement/orange-money/retour/",
                "cancel_url": f"{settings.SITE_URL}/paiement/orange-money/annulation/",
                "notif_url": f"{settings.SITE_URL}/api/paiements/orange-money/notification/",
                "lang": "fr",
                "reference": transaction_id
            }

            # Créer l'enregistrement de paiement
            paiement = Paiement.objects.create(
                commande=commande,
                reference_transac=transaction_id,
                nom_methode="orange_money",
                montant=commande.montant_total,
                statut="en_attente"
            )

            # Créer l'enregistrement Orange Money
            orange_payment = PaiementOrangeMoney.objects.create(
                paiement=paiement,
                numero_telephone=numero_telephone,
                code_transaction=transaction_id,
                statut_orange="pending"
            )

            # En mode démo, simuler une réponse
            return {
                "success": True,
                "transaction_id": transaction_id,
                "payment_url": f"https://webpay.orange.com/demo/{transaction_id}",
                "message": "Paiement Orange Money initié avec succès"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def verifier_statut_paiement(self, transaction_id):
        """Vérifier le statut d'un paiement Orange Money"""
        try:
            # En mode démo, retourner un statut simulé
            return {
                "transaction_id": transaction_id,
                "status": "success",
                "amount": 1000,
                "currency": "XOF"
            }
        except Exception as e:
            return {"error": str(e)}

class CarteBancaireService:
    def __init__(self):
        self.api_url = getattr(settings, 'STRIPE_API_URL', 'https://api.stripe.com/v1')
        self.secret_key = getattr(settings, 'STRIPE_SECRET_KEY', 'sk_test_demo_key')
        self.publishable_key = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', 'pk_test_demo_key')

    def valider_carte(self, numero_carte, cvv, date_expiration):
        """Valider les informations de carte bancaire"""
        # Validation basique (à améliorer en production)
        if len(numero_carte.replace(' ', '').replace('-', '')) != 16:
            return False, "Numéro de carte invalide"
        
        if len(cvv) not in [3, 4]:
            return False, "CVV invalide"
        
        try:
            mois, annee = date_expiration.split('/')
            if int(mois) < 1 or int(mois) > 12:
                return False, "Mois d'expiration invalide"
            
            date_exp = datetime(int(annee), int(mois), 1)
            if date_exp < datetime.now():
                return False, "Carte expirée"
        except:
            return False, "Date d'expiration invalide"
        
        return True, "Carte valide"

    def detecter_type_carte(self, numero_carte):
        """Détecter le type de carte bancaire"""
        numero = numero_carte.replace(' ', '').replace('-', '')
        
        if numero.startswith('4'):
            return 'visa'
        elif numero.startswith(('5', '2')):
            return 'mastercard'
        elif numero.startswith(('34', '37')):
            return 'american_express'
        else:
            return 'inconnu'

    def initier_paiement(self, commande, numero_carte, cvv, date_expiration, nom_porteur):
        """Initier un paiement par carte bancaire"""
        try:
            # Valider la carte
            valide, message = self.valider_carte(numero_carte, cvv, date_expiration)
            if not valide:
                return {"success": False, "error": message}

            # Générer un token sécurisé et masquer le numéro
            token_paiement = f"tok_{uuid.uuid4().hex}"
            numero_masque = f"****-****-****-{numero_carte[-4:]}"
            type_carte = self.detecter_type_carte(numero_carte)

            # Créer l'enregistrement de paiement
            paiement = Paiement.objects.create(
                commande=commande,
                reference_transac=token_paiement,
                nom_methode="carte_bancaire",
                montant=commande.montant_total,
                statut="en_attente"
            )

            # Créer l'enregistrement carte bancaire
            carte_payment = PaiementCarteBancaire.objects.create(
                paiement=paiement,
                numero_carte_masque=numero_masque,
                type_carte=type_carte,
                token_paiement=token_paiement,
                statut_banque="pending"
            )

            # En mode démo, simuler une autorisation
            carte_payment.code_autorisation = "AUTH123"
            carte_payment.statut_banque = "authorized"
            carte_payment.date_autorisation = datetime.now()
            carte_payment.save()

            paiement.statut = "complete"
            paiement.save()

            return {
                "success": True,
                "transaction_id": token_paiement,
                "authorization_code": "AUTH123",
                "message": "Paiement par carte autorisé avec succès"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def capturer_paiement(self, token_paiement):
        """Capturer un paiement autorisé"""
        try:
            carte_payment = PaiementCarteBancaire.objects.get(token_paiement=token_paiement)
            
            if carte_payment.statut_banque == "authorized":
                carte_payment.statut_banque = "captured"
                carte_payment.save()
                
                carte_payment.paiement.statut = "complete"
                carte_payment.paiement.save()
                
                return {"success": True, "message": "Paiement capturé"}
            else:
                return {"success": False, "error": "Paiement non autorisé"}
                
        except PaiementCarteBancaire.DoesNotExist:
            return {"success": False, "error": "Paiement non trouvé"}