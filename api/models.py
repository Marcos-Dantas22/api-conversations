from django.db import models
from .utils import StateConversationStatus, StateMessageStatus
import uuid
from django.db.models import Q

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
        on_delete=models.CASCADE
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

class LeadInfos(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        verbose_name="Conversa",
        on_delete=models.CASCADE
    )
    type_property = models.CharField(max_length=100, null=True, blank=True)
    neighborhood = models.CharField(max_length=100, null=True, blank=True)
    price_track = models.CharField(max_length=100, null=True, blank=True)
    rooms = models.IntegerField(null=True, blank=True)
    urgency = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Busca de imovel"
        verbose_name_plural = "Buscas de imoveis"

    def __str__(self):
        return f"LeadInfos {self.id}"

class Property(models.Model):
    type_property = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    price_track = models.CharField(max_length=100)
    rooms = models.IntegerField()
    
    class Meta:
        verbose_name = "Imóvel"
        verbose_name_plural = "Imóveis"

    def __str__(self):
        return f"{self.type_property} - {self.neighborhood}"

    def lead_match_count(self):
        return LeadInfos.objects.filter(
            Q(type_property__icontains=self.type_property ) &
            Q(neighborhood__icontains=self.neighborhood ) &
            # Q(price_track__icontains=self.price_track ) &
            Q(rooms=self.rooms)
        ).count()