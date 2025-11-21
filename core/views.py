# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from core.agent import AIAgent
from core.gemini_api import GeminiClient
from core.session_state import session
from core.jwt_utils import decode_token

class ChatView(APIView):
    def post(self, request):
        user_message = request.data.get('message') or ""

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            decoded_data = decode_token(token)

            if decoded_data:
                session.is_authenticated = True
                session.user_id = decoded_data.get("id")
                session.role = decoded_data.get("role")
                session.token = auth_header
            else:
                session.is_authenticated = False
                session.role = "GUEST"
        else:
            session.is_authenticated = False
            session.role = "GUEST"

        llm = GeminiClient()
        agent = AIAgent(llm)
        response = agent.handle_message(user_message)

        return Response({
            "response": response,
            "role": session.role,
            "authenticated": session.is_authenticated
        })
