from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'password']
    ordering = ['-created_at']

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Sécurité', {
            'fields': ('password',)
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
