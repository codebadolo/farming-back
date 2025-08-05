
from django.contrib import admin
from .models import APIConfiguration, APIAccessToken, APIRequestLog, APIVersion

@admin.register(APIConfiguration)
class APIConfigurationAdmin(admin.ModelAdmin):
    list_display = ['api_name', 'is_active', 'last_updated']

@admin.register(APIAccessToken)
class APIAccessTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_email', 'token_short', 'is_active']
    list_filter = ['is_active', 'created_at']

@staticmethod
def get_user_email(self, obj):
        return obj.user.email
get_user_email.short_description = 'Email Utilisateur'
    
def get_short_token(self, obj):
        return f"{obj.token[:10]}..." if obj.token else ""
get_short_token.short_description = 'Token (abbrégé)'

admin.site.register(APIAccessToken, APIAccessTokenAdmin)
def token_short(self, obj):
        return f"{obj.token[:10]}..." if obj.token else ""
token_short.short_description = "Token"

@admin.register(APIRequestLog)
class APIRequestLogAdmin(admin.ModelAdmin):
    list_display = ['endpoint', 'method', 'user', 'status_code', 'response_time', 'ip_address', 'created_at']
    list_filter = ['method', 'status_code']

@admin.register(APIVersion)
class APIVersionAdmin(admin.ModelAdmin):
    list_display = ['version', 'is_current', 'release_date']
    list_filter = ['is_current']
    readonly_fields = ['version']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    
    def get_queryset(self, request):
        return APIVersion.objects.filter(is_current=True)