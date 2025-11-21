from core.session_state import session
import requests

class GetInventoryTask:
    def __init__(self, base_url="http://localhost:8083/eggs/totalQuantity"):
        self.base_url = base_url

    def execute(self):
        headers = {}

        if session.is_authenticated and session.token:
            print(session.token)
            headers["Authorization"] = f"{session.token}"

        try:
            response = requests.get(self.base_url, headers=headers)

            if response.status_code == 200:
                return response.json()
            
            elif response.status_code == 401:
                return "🔐 No tienes autorización para acceder al inventario."
            
            else:
                return f"⚠️ Error consultando inventario: ({response.status_code}) {response.text}"
            
        except Exception as e:
            return f"🚨 Error al conectar al microservicio: {str(e)}"
