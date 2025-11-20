from core.tasks import GetTodaySalesTask, RegisterUserTask
from core.tasks.get_inventory_task import GetInventoryTask
from core.gemini_api import GeminiClient
from core.session_state import session

REQUIRED_REGISTRATION_FIELDS = [
    "username",
    "password",
    "email",
    "full_name",
    "document",
    "phone_number",
    "address"
]

def require_auth(func):
    def wrapper(self, message):
        if not session.token:
            session.memory["pending_action"] = func.__name__
            return "🔐 Necesito que inicies sesión antes de continuar. ¿Quieres hacerlo ahora?"
        return func(self, message)
    return wrapper


class AIAgent:
    def __init__(self, llm: GeminiClient):
        self.llm = llm

        self.handlers = {
            "ventas": self.handle_sales,
            "ventas_hoy": self.handle_sales,
            "ventas_del_dia": self.handle_sales,
            "ventas_diarias": self.handle_sales,
            "inventario": self.handle_inventory,
            "ver_inventario": self.handle_inventory,
            "productos": self.handle_inventory,
            "registrar_usuario": self.handle_register_user
        }

    def handle_message(self, message: str):

        if session.is_registering:
            return self._continue_registration(message)

        intent = self.llm.detect_intent(message)
        print(f"DEBUG INTENT -> {intent}")

        handler = self.handlers.get(intent)

        if handler:
            return handler(message)

        return self.llm.generate_response(
            f"El usuario dijo: {message}. Responde amable como asistente del ERP."
        )

    def _continue_registration(self, message: str):

        field = session.pending_field
        session.registration_data[field] = message.strip()

        index = REQUIRED_REGISTRATION_FIELDS.index(field)
        if index + 1 < len(REQUIRED_REGISTRATION_FIELDS):
            session.pending_field = REQUIRED_REGISTRATION_FIELDS[index + 1]
            return f"👌 Genial. Ahora dime tu **{session.pending_field}**."
        
        task = RegisterUserTask(session.registration_data)
        api_result = task.execute()

        session.is_registering = False
        session.pending_field = None
        session.registration_data = {}

        return f"🎉 Registro completado.\n\n{api_result}"

    @require_auth
    def handle_sales(self, message: str):
        task = GetTodaySalesTask()
        data = task.execute()
        return self.llm.generate_response(
            f"Consulta: {message}",
            data=data
        )
    
    @require_auth
    def handle_inventory(self, message: str):

        if session.role != "ADMIN" or "EMPLOYEE":
            return "⛔ No tienes permisos para consultar inventario."

        task = GetInventoryTask()
        result = task.execute()

        if isinstance(result, str):
            return result

        # Si devolvió una lista, formatear bonito
        formatted = "\n".join([f"📦 {item['name']} - {item['stock']} unidades" for item in result])

        return f"📊 Inventario actual:\n{result}"

    def handle_register_user(self, message: str):

        if session.is_registering:
            return self._continue_registration(message)

        session.is_registering = True
        session.registration_data = {}
        session.pending_field = REQUIRED_REGISTRATION_FIELDS[0]

        return f"📝 Perfecto, vamos a crear tu cuenta.\n¿Cuál será tu **{session.pending_field}**?"

