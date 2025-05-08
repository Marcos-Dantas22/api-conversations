from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from .models import Conversation, Message
from .serializers import WebhookEventSerializer, ConversationSerializer
from django.utils.dateparse import parse_datetime
from .utils import StateConversationStatus, StateMessageStatus
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

class WebhookView(APIView):
    @extend_schema(
        summary="Recebe eventos do webhook",
        description="Processa eventos de criação de conversa, nova mensagem ou encerramento de conversa.",
        request=WebhookEventSerializer,
        responses={200: OpenApiExample(
            'Sucesso', value={"detail": "Evento processado com sucesso."}
        )}
    )
    def post(self, request):
        serializer = WebhookEventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        event_type = serializer.validated_data["type"]
        data = serializer.validated_data["data"]
        timestamp = serializer.validated_data["timestamp"]

        if event_type == "NEW_CONVERSATION":
            # Verificar se o ID da conversa já existe
            if "id" not in data:
                return Response({"error": "Conversation ID e obrigatorio."}, status=status.HTTP_400_BAD_REQUEST)

            if Conversation.objects.filter(id=data["id"]).exists():
                return Response({"error": f"Conversation ID {data['id']} já existe."}, status=status.HTTP_400_BAD_REQUEST)

            Conversation.objects.create(
                id=data["id"], state=StateConversationStatus.OPEN, created_at=timestamp
            )
        
        elif event_type == "NEW_MESSAGE":
            # Verificar se todos os campos necessários estão presentes
            if not all(key in data for key in ["id", "conversation_id", "content", "direction"]):
                return Response({"error": "Message ID, conversation ID, content, e direction são obrigatorios."}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar se o ID da mensagem já existe
            if Message.objects.filter(id=data["id"]).exists():
                return Response({"error": f"Message com essa ID {data['id']} já existe."}, status=status.HTTP_400_BAD_REQUEST)

            conversation = get_object_or_404(Conversation, id=data["conversation_id"])

            # Verificar se o conteúdo da mensagem não está vazio
            if not data["content"].strip():
                return Response({"error": "Message content não pode ser vazia."}, status=status.HTTP_400_BAD_REQUEST)

            if not data["id"].strip():
                return Response({"error": "Message ID não pode ser vazia."}, status=status.HTTP_400_BAD_REQUEST)

            Message.objects.create(
                id=data["id"],
                state=data["direction"],
                content=data["content"],
                created_at=timestamp,
                conversation=conversation,
            )
        
        elif event_type == "CLOSE_CONVERSATION":
            # Verificar se o ID da conversa para fechar foi fornecido
            if "id" not in data:
                return Response({"error": "Conversation ID e obrigatorio para fechar a conversa."}, status=status.HTTP_400_BAD_REQUEST)

            conversation = get_object_or_404(Conversation, id=data["id"])
            conversation.state = StateConversationStatus.CLOSED
            conversation.finish_at = timestamp
            conversation.save()

        return Response({"detail": "Evento processado com sucesso."}, status=status.HTTP_200_OK)

class ConversationDetailView(APIView):
    @extend_schema(
        summary="Detalhes de uma conversa",
        description="Retorna todas as informações da conversa com o ID fornecido, incluindo mensagens.",
        parameters=[
            OpenApiParameter(name='id', type=str, location=OpenApiParameter.PATH, required=True, description='ID da conversa')
        ],
        responses={200: ConversationSerializer}
    )
    def get(self, request, id):
        conversation = get_object_or_404(Conversation, id=id)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

def conversation_list_view(request):
    """
        View HTML: Lista todas as conversas existentes, ordenadas da mais recente para a mais antiga.
        Rota usada para frontend visual com Django Templates.
    """
    conversations = Conversation.objects.all().order_by('-created_at')
    return render(request, 'api/conversation_list.html', {'conversations': conversations})

def conversation_detail_view(request, id):
    """
        View HTML: Mostra os detalhes de uma conversa específica (mensagens incluídas).
        Ideal para navegação e visualização de histórico de mensagens no frontend.
    """
    conversation = get_object_or_404(Conversation, id=id)
    messages = Message.objects.filter(conversation=conversation).order_by('created_at')
    return render(request, 'api/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages
    })