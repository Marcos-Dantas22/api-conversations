from django.contrib import admin
from .models import Conversation, Message, FailedWebhookEvent

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'created_at', 'finish_at')
    list_filter = ('state', 'created_at')
    search_fields = ('id', 'state')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'state', 'content', 'created_at')
    list_filter = ('state', 'created_at', 'conversation')
    search_fields = ('content', 'conversation__id', 'state')

class FailedWebhookEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'data', 'timestamp', 'error_message','retry_count', 'last_retry_at','created_at')
    search_fields = ('id', 'error_message')

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(FailedWebhookEvent, FailedWebhookEventAdmin)
