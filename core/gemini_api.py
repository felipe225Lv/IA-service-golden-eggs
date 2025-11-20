import google.generativeai as genai
from django.conf import settings
import os
import json
import re
import logging
from core.session_state import session

logger = logging.getLogger("GeminiClient")


CONTEXT_PATH = os.path.join(settings.BASE_DIR, "core", "company_context.txt")

try:
    with open(CONTEXT_PATH, "r", encoding="utf-8") as f:
        COMPANY_CONTEXT = f.read()
except Exception:
    COMPANY_CONTEXT = ""
    logger.warning("⚠ No se pudo cargar el contexto empresarial")


class GeminiClient:
    """
    Maneja toda comunicación con Gemini:
    - Detección de intención
    - Respuestas estilo asistente
    - Extracción de datos estructurados cuando se requiera
    """

    INTENT_OPTIONS = {
        "ventas_hoy",
        "inventario",
        "clientes",
        "creditos",
        "registrar_usuario",
        "login",
        "otra"
    }

    def __init__(self, model_name="models/gemini-2.5-flash"):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name)

    def detect_intent(self, message: str) -> str:
        """
        Solo detecta intención si no hay una acción en curso.
        Si el usuario ya está en un flujo (ej. registro), NO se cambia el intent.
        """
        if session.pending_action or getattr(session, "is_registering", False):
            return session.pending_action or "registrar_usuario"

        prompt = f"""
        {COMPANY_CONTEXT}

        Analiza la frase del usuario y responde SOLO una palabra de esta lista:

        {list(self.INTENT_OPTIONS)}

        Si no encaja con ninguna opción, responde: "otra".

        Usuario: "{message}"
        """

        try:
            result = self.model.generate_content(prompt)
            intent = result.text.strip().lower()
            return intent if intent in self.INTENT_OPTIONS else "otra"

        except Exception as e:
            logger.error(f"❌ Error detectando intención: {e}")
            return "otra"

    def generate_response(self, user_message: str, data=None) -> str:
        """
        Genera una respuesta amable y estructurada en contexto del sistema.
        """
        prompt = f"""
        {COMPANY_CONTEXT}

        Usuario: "{user_message}"
        {f"Datos relevantes: {data}" if data else ""}

        Responde como un asistente profesional de GoldenEggs ERP:
        - Corto y natural
        - Directo al punto
        - No inventes datos si no existen
        - Habla en español
        """

        try:
            result = self.model.generate_content(prompt)
            return result.text.strip()

        except Exception as e:
            logger.error(f"⚠ Error generando respuesta: {e}")
            return "Lo siento, hubo un error generando la respuesta."

    def extract_user_data(self, user_message: str) -> dict:
        """
        Convierte una frase del usuario en un JSON estandarizado.
        Esta función se usa SOLO si el usuario ya expresó intención de registrarse.
        """
        prompt = f"""
        Extrae información del siguiente mensaje del usuario y conviértelo
        en JSON válido. Si no tienes un dato, deja null.

        Campos requeridos:
        - username
        - password
        - email
        - full_name
        - document
        - phone_number
        - address
        - role

        Usuario dijo: "{user_message}"

        Respuesta SOLO debe ser JSON sin texto extra.
        """

        try:
            result = self.model.generate_content(prompt)
            text = re.sub(r"```(\w+)?|```", "", result.text).strip()
            user_data = json.loads(text)

        except Exception as e:
            logger.error(f"❌ Error parseando JSON: {e}, respuesta recibida: {result.text if 'result' in locals() else 'n/a'}")
            return {}

        # Seguridad: todos los registros del chat → CUSTOMER
        user_data["role"] = "CUSTOMER"

        return user_data
