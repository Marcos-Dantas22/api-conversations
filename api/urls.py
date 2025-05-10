from django.urls import path
from .views import (
    WebhookView, ConversationDetailView, 
    conversation_detail_view, conversation_list_view, delete_conversation,
    leadinfos_detail, leadinfos_list, interface_home

)
urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='webhook'),
    path('conversations/<uuid:id>/', ConversationDetailView.as_view(), name='conversation-detail'),

    path('interface/conversas/', conversation_list_view, name='conversation_list'),
    path('interface/conversas/<slug:id>/', conversation_detail_view, name='conversation_detail'),
    path('interface/conversas/delete/<slug:id>/', delete_conversation, name='delete_conversation'),

    path('interface/imoveis/', leadinfos_list, name='leadinfos_list'),
    path('interface/imoveis/<slug:id>/', leadinfos_detail, name='leadinfos_detail'),

    path('interface', interface_home, name='interface_home'),
    
]
