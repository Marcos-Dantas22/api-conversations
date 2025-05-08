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