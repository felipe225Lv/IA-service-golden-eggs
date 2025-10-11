from core.tasks import GetTodaySalesTask, UnknownTask, RegisterUserTask
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
        elif intent == "registrar_usuario":
            return self.handle_register_user(message)
        else:
            # Si no se detecta intención técnica, responder como chat natural
            return self.llm.generate_response(f"Responde amablemente a: {message}")

    def handle_sales(self):
        task = GetTodaySalesTask()
        data = task.execute()
        return self.llm.generate_response("Mostrar resumen de ventas del día.", data)

    def handle_inventory(self):
        # Ejemplo futuro
        return "🔧 (Inventario aún no implementado)"

    def handle_users(self):
        # Ejemplo futuro
        return "🧑 (Consulta de usuarios aún no implementada)"

    def handle_register_user(self, message):
        """
        Extrae los datos del mensaje y ejecuta la tarea de registro de usuario.
        """
        # Aquí el modelo debe extraer datos o recibirlos del front en formato JSON
        try:
            user_data = self.llm.extract_user_data(message)
            task = RegisterUserTask(user_data)
            result = task.execute()
            return result
        except Exception as e:
            return f"❌ No fue posible procesar el registro: {str(e)}"
