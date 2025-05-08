from django.contrib import admin
from .models import Conversation, Message

# Registro do modelo Conversation
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'created_at', 'finish_at')
    list_filter = ('state', 'created_at')
    search_fields = ('id', 'state')
    date_hierarchy = 'created_at'

# Registro do modelo Message
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'state', 'content', 'created_at')
    list_filter = ('state', 'created_at', 'conversation')
    search_fields = ('content', 'conversation__id', 'state')
    date_hierarchy = 'created_at'

# Registrando os modelos com suas classes admin
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
