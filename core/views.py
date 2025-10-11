from rest_framework.views import APIView
from rest_framework.response import Response
from core.agent import AIAgent
from core.gemini_api import GeminiClient

class ChatView(APIView):
    def post(self, request):
        user_message = request.data.get('message') or request.data.get('question') or ""
        
        llm = GeminiClient() 
        agent = AIAgent(llm)       
        response = agent.handle_message(user_message)

        return Response({"response": response})
