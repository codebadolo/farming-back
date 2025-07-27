from rest_framework import serializers
from .models import MethodePaiement, Paiement

class MethodePaiementSerializer(serializers.ModelSerializer):
     class Meta:
        model = MethodePaiement
        fields = "__all__"
        
class PaiementSerializer(serializers.ModelSerializer):
   class Meta:
      model = Paiement
      fields = "__all__"