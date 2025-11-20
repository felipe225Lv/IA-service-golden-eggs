import requests
from core.session_state import session

class GetInventoryTask:
    def __init__(self, base_url="http://localhost:8081/eggs/totalQuantity"):
        self.base_url = base_url

    def execute(self):
        headers = {}

        if session.token:
            headers["Authorization"] = f"Bearer {session.token}"

        try:
            response = requests.get(self.base_url, headers=headers)

            if response.status_code == 200:
                return response.json()
            
            elif response.status_code == 401:
                return "🔐 Necesitas iniciar sesión para consultar el inventario."
            
            else:
                return f"⚠️ Error consultando inventario: ({response.status_code}) {response.text}"
            
        except Exception as e:
            return f"🚨 Error al conectar al microservicio: {str(e)}"

