from django.db.models import TextChoices

class StateConversationStatus(TextChoices):
    OPEN = 'OPEN', 'Aberto'
    CLOSED = 'CLOSED', 'Fechado',

class StateMessageStatus(TextChoices):
    SENT = 'SENT', 'Enviado'
    RECEIVED = 'RECEIVED', 'Recebido',