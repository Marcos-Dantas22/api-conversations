from django.db import models
from .utils import StateConversationStatus, StateMessageStatus
import uuid

# Create your models here.
class Conversation(models.Model):
    state = models.CharField(
        verbose_name="Estado da Conversa",
        max_length=20,
        help_text="Estado da Conversa",
        choices=StateConversationStatus.choices, 
    )
    created_at = models.DateTimeField(
        verbose_name="criado em",
        help_text="data de criação",
    )

    finish_at = models.DateTimeField(
        verbose_name="finalizado em",
        help_text="data de finalização",
        null=True,
        blank=True,
    )

    id = models.SlugField(
        primary_key=True,
        verbose_name="Id",
        max_length=150,
        unique=True,
        default=uuid.uuid4
    )
    

    class Meta:
        verbose_name = "Conversa"
        verbose_name_plural = "Conversas"

    def __str__(self):
        return f"Conversa {self.id}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        verbose_name="Conversa",
        on_delete=models.CASCADE,
        default=None
    )
    content = models.CharField(
        verbose_name="Conteudo",
        max_length=1000,
        help_text="Conteudo da Mensagem",
    )
    state = models.CharField(
        verbose_name="Estado da Mensagem",
        max_length=20,
        help_text="Estado da Mensagem",
        choices=StateMessageStatus.choices, 
    )

    created_at = models.DateTimeField(
        verbose_name="criado em",
        help_text="data de criação",
    )

    id = models.SlugField(
        primary_key=True,
        verbose_name="Id",
        max_length=150,
        unique=True,
        default=uuid.uuid4
    )

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"

    def __str__(self):
        return f"Mensagem {self.id}"
    

class FailedWebhookEvent(models.Model):
    type = models.CharField(max_length=50)
    data = models.JSONField()
    timestamp = models.DateTimeField()
    error_message = models.TextField()
    retry_count = models.IntegerField(default=0)
    last_retry_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Evento do Webhook com Falha"
        verbose_name_plural = "Eventos do Webhook com Falha"

    def __str__(self):
        return f"Event {self.id}"

class LeadInformantion(models.Model):
    conversation_id = models.ForeignKey(
        Conversation,
        verbose_name="Conversation",
        on_delete=models.CASCADE,
        related_name='lead_info',
    )
   
    type_property = models.CharField(max_length=100, null=True, blank=True)
    neighborhood = models.CharField(max_length=100, null=True, blank=True)
    price_track = models.CharField(max_length=100, null=True, blank=True)
    rooms = models.IntegerField(null=True, blank=True)
    urgency = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Informações de imovel"
        verbose_name_plural = "Informações de imoveis"

    def __str__(self):
        return f"LeadInformation {self.id}"