from rest_framework.views import APIView
from rest_framework.response import Response
from intelligence.models import Conversation

class ConversationList(APIView):
    def get(self, request):
        data = Conversation.objects.values()
        return Response(list(data))
