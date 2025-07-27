from django.contrib import admin
from .models import User, Adresse, Client, Vendeur

# Modele pour les utilisateurs.
admin.site.register(User)
admin.site.register(Adresse)
admin.site.register(Client)
admin.site.register(Vendeur)
