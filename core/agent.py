from core.tasks import GetTodaySalesTask, UnknownTask
from core.client import MicroserviceClient
from core.gemini_api import GeminiClient


class AIAgent:
    def __init__(self, llm: GeminiClient):
        self.llm = llm

    def handle_message(self, message):
        intent = self.llm.detect_intent(message)

        if intent == "ventas":
            return self.handle_sales()
        elif intent == "inventario":
            return self.handle_inventory()
        elif intent == "usuarios":
            return self.handle_users()
        else:
            # Si no se detecta intención técnica, responder como chat natural
            return self.llm.generate_response(f"Responde amablemente a: {message}")
