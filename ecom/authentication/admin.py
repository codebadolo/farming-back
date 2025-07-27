from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, VendeurProfile, AcheteurProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Administration des utilisateurs personnalisés"""
    
    list_display = ('email', 'nom', 'prenom', 'role', 'status', 'date_inscription')
    list_filter = ('role', 'status', 'date_inscription')
    search_fields = ('email', 'nom', 'prenom', 'telephone')
    ordering = ('-date_inscription',)
    
    fieldsets = list(UserAdmin.fieldsets) + [
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'telephone', 'role', 'status')
        }),
    ]
    
    add_fieldsets = list(UserAdmin.add_fieldsets) + [
        ('Informations personnelles', {
            'fields': ('email', 'nom', 'prenom', 'telephone', 'role')
        }),
    ]


@admin.register(VendeurProfile)
class VendeurProfileAdmin(admin.ModelAdmin):
    """Administration des profils vendeurs"""
    
    list_display = ('nom_entreprise', 'utilisateur', 'status_validation', 'date_creation')
    list_filter = ('status_validation', 'date_creation', 'date_validation')
    search_fields = ('nom_entreprise', 'utilisateur__nom', 'utilisateur__prenom')
    readonly_fields = ('date_creation', 'date_validation')
    
    fieldsets = (
        ('Informations entreprise', {
            'fields': ('utilisateur', 'nom_entreprise', 'description', 'logo')
        }),
        ('Contact', {
            'fields': ('adresse', 'telephone_entreprise')
        }),
        ('Validation', {
            'fields': ('status_validation', 'date_creation', 'date_validation')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and 'status_validation' in form.changed_data:
            if obj.status_validation == VendeurProfile.StatusValidation.VALIDE:
                from django.utils import timezone
                obj.date_validation = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(AcheteurProfile)
class AcheteurProfileAdmin(admin.ModelAdmin):
    """Administration des profils acheteurs"""
    
    list_display = ('utilisateur', 'preferences_notifications', 'newsletter', 'date_creation')
    list_filter = ('preferences_notifications', 'newsletter', 'date_creation')
    search_fields = ('utilisateur__nom', 'utilisateur__prenom', 'utilisateur__email')
    readonly_fields = ('date_creation',)