from rest_framework import serializers
from api.models import Conversation, Message

class WebhookEventSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["NEW_CONVERSATION", "NEW_MESSAGE", "CLOSE_CONVERSATION"])
    timestamp = serializers.DateTimeField()
    data = serializers.DictField()

class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'state', 'created_at', 'finish_at', 'messages']

    def get_messages(self, obj):
        dict_response = []
        conversation_id = obj.id
        
        if conversation_id:
            for message in Message.objects.filter(conversation_id=conversation_id).order_by('created_at'):
                dict_response.append({
                    'id': message.id, 
                    'state': message.state, 
                    'content': message.content, 
                    'created_at': message.created_at,
                })

            return dict_response
        return ''