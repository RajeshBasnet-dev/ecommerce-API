from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'order', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at', 'sender', 'receiver')
    search_fields = ('sender__username', 'receiver__username', 'order__id')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 25
    
    actions = ['mark_as_read', 'mark_as_unread']

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected messages as unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)