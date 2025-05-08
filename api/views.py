from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import WebhookEventSerializer, ConversationSerializer
from django.utils.dateparse import parse_datetime
from .utils import StateConversationStatus, StateMessageStatus

class WebhookView(APIView):
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
    def get(self, request, id):
        conversation = get_object_or_404(Conversation, id=id)
        serializer = ConversationSerializer(conversation)
        print(serializer.data)
        return Response(serializer.data)
