from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from .models import Conversation, Message, FailedWebhookEvent, LeadInformantion
from .serializers import WebhookEventSerializer, ConversationSerializer, SuccessResponseSerializer, ErrorResponseSerializer
from .utils import StateConversationStatus
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.utils import OpenApiResponse
from realmate_challenge.authentication import ApiKeyAuthenticationPersonal
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .geminy import extrair_lead_info
from django.conf import settings

class WebhookView(APIView):
    authentication_classes = [ApiKeyAuthenticationPersonal]

    @extend_schema(
        summary="Recebe eventos do webhook",
        description="Processa eventos de criação de conversa, nova mensagem ou encerramento de conversa.",
        request=WebhookEventSerializer,
        examples=[
            OpenApiExample(
                name="Nova Conversa",
                summary="Evento de nova conversa",
                value={
                    "type": "NEW_CONVERSATION",
                    "timestamp": "2025-05-09T18:30:00Z",
                    "data": {
                        "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a",
                    }
                },
                request_only=True
            ),
            OpenApiExample(
                name="Nova Mensagem",
                summary="Evento de nova mensagem",
                value={
                    "type": "NEW_MESSAGE",
                    "timestamp": "2025-05-09T18:30:00Z",
                    "data": {
                        "id": "49108c71-4dca-4af3-9f32-61bc745926e2",
                        "direction": "RECEIVED",
                        "content": "Olá, tudo bem?",
                        "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a",
                    }
                },
                request_only=True
            ),
            OpenApiExample(
                name="Encerrar Conversa",
                summary="Evento de encerramento de conversa",
                value={
                    "type": "CLOSE_CONVERSATION",
                    "timestamp": "2025-05-09T18:30:00Z",
                    "data": {
                        "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a",
                    }
                },
                request_only=True
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=SuccessResponseSerializer,
                description="Evento processado com sucesso.",
                examples=[
                    OpenApiExample(
                        name="Sucesso",
                        value={"detail": "Evento processado com sucesso."},
                        response_only=True
                    )
                ]
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Erro de Validação",
                examples=[
                    OpenApiExample(
                        name="Mensagem duplicada",
                        value={"error": "Mensagem com esse ID já existe."},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="Campos obrigatórios ausentes",
                        value={"error": "id, conversation_id , content, e direction são obrigatorios."},
                        response_only=True
                    ),
                    OpenApiExample(
                        name="Conversa já fechada",
                        value={"error": "Conversa fechada, não é possivel processar novas mensagens."},
                        response_only=True
                    )
                ]
            ),
            401: OpenApiResponse(
                response=SuccessResponseSerializer,  # ou outro se quiser
                description="Chave de API ausente ou inválida.",
                examples=[
                    OpenApiExample(
                        name="Credenciais inválidas.",
                        value={"detail": "Credenciais inválidas"},
                        response_only=True
                    )
                ]
            ),
            500: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Erro Interno",
                examples=[
                    OpenApiExample(
                        name="Erro inesperado",
                        value={"error": "Erro ao processar evento. Será reprocessado."},
                        response_only=True
                    )
                ]
            ),
        }
    )
    def post(self, request):
        serializer = WebhookEventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        event_type = serializer.validated_data["type"]
        data = serializer.validated_data["data"]
        timestamp = serializer.validated_data["timestamp"]

        try:
            if event_type == "NEW_CONVERSATION":
                if "id" not in data:
                    return Response({"error": "id é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

                if Conversation.objects.filter(id=data["id"]).exists():
                    return Response({"error": f"Conversa com essa ID {data['id']} já existe."}, status=status.HTTP_400_BAD_REQUEST)

                Conversation.objects.create(
                    id=data["id"], state=StateConversationStatus.OPEN, created_at=timestamp
                )
            
            elif event_type == "NEW_MESSAGE":
                if not all(key in data for key in ["id", "conversation_id", "content", "direction"]):
                    return Response({"error": "Message ID, conversation ID, content e direction são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

                if Message.objects.filter(id=data["id"]).exists():
                    return Response({"error": f"Mensagem com essa ID {data['id']} já existe."}, status=status.HTTP_400_BAD_REQUEST)

                conversation = Conversation.objects.filter(id=data["conversation_id"]).first()
                if not conversation:
                    return Response({"error": f"Conversa com essa ID {data['id']} não existe."}, status=status.HTTP_400_BAD_REQUEST)

                if not data["content"].strip():
                    return Response({"error": "Message content não pode ser vazio."}, status=status.HTTP_400_BAD_REQUEST)

                if not data["id"].strip():
                    return Response({"error": "Message ID não pode ser vazio."}, status=status.HTTP_400_BAD_REQUEST)
                
                if conversation.state == StateConversationStatus.CLOSED:
                    return Response({"error": "Conversa fechada, não é possivel processar novas mensagens."}, status=status.HTTP_400_BAD_REQUEST)

                if data['direction'] == "RECEIVED" and settings.DEBUG == False:
                    infos = extrair_lead_info(data["content"])
                    if infos:
                        LeadInformantion.objects.create(
                            conversation_id=conversation,
                            type_property=infos.get("type_property"),
                            neighborhood=infos.get("neighborhood"),
                            price_track=infos.get("price_track"),
                            rooms=infos.get("rooms"),
                            urgency=infos.get("urgency"),
                        )

                Message.objects.create(
                    id=data["id"],
                    state=data["direction"],
                    content=data["content"],
                    created_at=timestamp,
                    conversation=conversation,
                )
            
            elif event_type == "CLOSE_CONVERSATION":
                if "id" not in data:
                    return Response({"error": "id é obrigatório para fechar a conversa."}, status=status.HTTP_400_BAD_REQUEST)

                conversation = get_object_or_404(Conversation, id=data["id"])
                conversation.state = StateConversationStatus.CLOSED
                conversation.finish_at = timestamp
                conversation.save()

        except Exception as e:
            FailedWebhookEvent.objects.create(
                type=event_type,
                data=data,
                timestamp=timestamp,
                error_message=str(e),
            )
            return Response({"error": "Erro ao processar evento. Será reprocessado."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "Evento processado com sucesso."}, status=status.HTTP_200_OK)

class ConversationDetailView(APIView):
    authentication_classes = [ApiKeyAuthenticationPersonal]

    @extend_schema(
        summary="Detalhes de uma conversa",
        description="Retorna todas as informações da conversa com o ID fornecido, incluindo mensagens.",
        parameters=[ 
            OpenApiParameter(
                name='id',
                type=str,
                location=OpenApiParameter.PATH,
                required=True,
                description='ID da conversa (UUID).'
            )
        ],
        responses={
            200: OpenApiResponse(
                response=ConversationSerializer,
                description="Detalhes da conversa retornados com sucesso.",
                examples=[
                    OpenApiExample(
                        name="Exemplo de conversa com mensagens",
                        value={
                            "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a",
                            "state": "OPEN",
                            "created_at": "2025-05-09T18:30:00Z",
                            "finish_at": None,
                            "messages": [
                                {
                                    "id": "49108c71-4dca-4af3-9f32-61bc745926e2",
                                    "state": "RECEIVED",
                                    "content": "Olá, tudo bem?",
                                    "created_at": "2025-05-09T18:31:00Z"
                                }
                            ]
                        },
                        response_only=True
                    )
                ]
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="ID inválido ou erro de validação.",
                examples=[
                    OpenApiExample(
                        name="ID inválido",
                        value={"error": "ID inválido ou não encontrado."},
                        response_only=True
                    )
                ]
            ),
            401: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Chave de API ausente ou inválida.",
                examples=[
                    OpenApiExample(
                        name="Credenciais inválidas",
                        value={"detail": "Credenciais inválidas"},
                        response_only=True
                    )
                ]
            )
        }
    )
    def get(self, request, id):
        conversation = Conversation.objects.filter(id=id).first()
        if not conversation:
            return Response({"error": "ID inválido ou não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

def conversation_list_view(request):
    conversations = Conversation.objects.all().order_by('-created_at')
    paginator = Paginator(conversations, 10)  # 10 por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'api/conversation_list.html', {
        'page_obj': page_obj
    })

@require_http_methods(["DELETE"])
def delete_conversation(request, id):
    try:
        conv = Conversation.objects.get(id=id)
        conv.delete()
        return JsonResponse({'message': 'Conversa apagada com sucesso.'})
    except Conversation.DoesNotExist:
        return JsonResponse({'message': 'Conversa não encontrada.'}, status=404)
    
def conversation_detail_view(request, id):
    conversation = get_object_or_404(Conversation, id=id)
    messages = Message.objects.filter(conversation=conversation).order_by('created_at')
    return render(request, 'api/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages
    })
