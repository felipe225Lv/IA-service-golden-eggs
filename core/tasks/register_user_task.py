import requests

class RegisterUserTask:
    """
    Tarea que maneja el registro de nuevos usuarios a través del microservicio de usuarios.
    """

    def __init__(self, user_data, base_url="http://localhost:8081/users/register/"):
        self.user_data = user_data
        self.base_url = base_url

    def execute(self):
        try:
            response = requests.post(self.base_url, json=self.user_data)
            if response.status_code == 201:
                return "✅ ¡Tu cuenta ha sido creada exitosamente en GoldenEggs! Ya puedes iniciar sesión."
            elif response.status_code == 400:
                return f"❌ Error al registrar el usuario. Detalles: {response.json()}"
            else:
                return f"⚠️ No se pudo registrar el usuario (Código {response.status_code})."
        except Exception as e:
            return f"🚨 Ocurrió un error al intentar registrar el usuario: {str(e)}"
