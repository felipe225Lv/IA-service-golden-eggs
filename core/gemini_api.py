import google.generativeai as genai
from django.conf import settings
import os
import json
import re

CONTEXT_PATH = os.path.join(settings.BASE_DIR, "core", "company_context.txt")

with open(CONTEXT_PATH, "r", encoding="utf-8") as f:
    COMPANY_CONTEXT = f.read()

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("models/gemini-2.5-flash")

    def detect_intent(self, message):
        prompt = f"""
        {COMPANY_CONTEXT}

        Usuario: "{message}"

        Analiza la intención del usuario y responde con una palabra clave:
        - "ventas_hoy" si pregunta por ventas del día
        - "inventario" si pregunta por disponibilidad o stock
        - "clientes" si habla sobre clientes o sus datos
        - "creditos" si menciona deudas, pagos o créditos
        - "registrar_usuario" si desea crear una nueva cuenta o registrarse
        - "otra" si no se reconoce
        """

        result = self.model.generate_content(prompt)
        intent = result.text.strip().lower()
        return intent if intent in ["ventas_hoy", "inventario", "clientes", "creditos", "registrar_usuario"] else "otra"

    
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
        
    def extract_user_data(self, user_message):
        """
        Usa el modelo de lenguaje para estructurar los datos del usuario en formato JSON.
        """
        prompt = f"""
        A partir del siguiente mensaje del usuario, genera un JSON **válido** y sin explicaciones adicionales,
        que contenga los campos necesarios para registrar un usuario en GoldenEggs:
        username, password, email, first_name, last_name, role, document, phone_number, address.
        Si algún dato falta, coloca null. 
        NO incluyas texto adicional ni etiquetas markdown (sin ```json ni ```).
        Solo imprime el JSON puro.
        
        Mensaje del usuario: "{user_message}"
        """

        result = self.model.generate_content(prompt)

        # Limpiar el texto de markdown y obtener el JSON real
        text = result.text.strip()
        text = re.sub(r"```json|```", "", text).strip()

        try:
            user_data = json.loads(text)
        except Exception as e:
            print("❌ Error al parsear el JSON generado por Gemini:", e)
            print("Texto recibido:", text)
            user_data = {}

        # 🔒 Forzar siempre el rol a CUSTOMER
        user_data["role"] = "CUSTOMER"
        return user_data


