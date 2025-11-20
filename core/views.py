from rest_framework.views import APIView
from rest_framework.response import Response
from core.agent import AIAgent
from core.gemini_api import GeminiClient
from core.session_state import SessionState
from core.jwt_utils import decode_token


class ChatView(APIView):
    def post(self, request):
        user_message = request.data.get('message') or request.data.get('question') or ""

        auth_header = request.headers.get("Authorization")
        session = SessionState()

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            # Intentar decodificar token
            user_data = decode_token(token)

            if user_data:
                session.is_authenticated = True
                session.user_id = user_data.get("id")
                session.role = user_data.get("role", "CUSTOMER")  # default por si no hay rol
            else:
                session.is_authenticated = False
                session.role = "GUEST"
        else:
            # Usuario no autenticado
            session.is_authenticated = False
            session.role = "GUEST"


        # --- 🧠 Procesar IA ---
        llm = GeminiClient()
        agent = AIAgent(llm)
        response = agent.handle_message(user_message)

        return Response({
            "response": response,
            "authenticated": session.is_authenticated,
            "role": session.role
        })
