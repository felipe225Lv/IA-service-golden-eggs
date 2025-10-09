import google.generativeai as genai
from django.conf import settings
import os

CONTEXT_PATH = os.path.join(settings.BASE_DIR, "core", "company_context.txt")

with open(CONTEXT_PATH, "r", encoding="utf-8") as f:
    COMPANY_CONTEXT = f.read()

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("models/gemini-2.5-pro")

    def detect_intent(self, message):
        prompt = f"""
        {COMPANY_CONTEXT}

        Usuario: "{message}"
        """
        result = self.model.generate_content(prompt)
        intent = result.text.strip().lower()
        return intent if intent in ["ventas_hoy", "inventario", "clientes", "creditos"] else "otra"
    
    def generate_response(self, user_message, data=None):
        prompt = f"""
        {COMPANY_CONTEXT}
        
        El usuario preguntó: "{user_message}".
        {f"Los datos obtenidos son: {data}." if data else ""}
        Redacta una respuesta clara y natural en español.
        """
        try:
            result = self.model.generate_content(prompt)
            return result.text.strip()
        except Exception as e:
            return f"Ocurrió un error al generar la respuesta: {str(e)}"

