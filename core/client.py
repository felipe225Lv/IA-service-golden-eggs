import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError
import logging
from .session_state import session


logger = logging.getLogger("MicroserviceClient")


class MicroserviceClient:

    def __init__(self, base_url: str = None):
        """
        base_url puede venir del env o configuraciones.
        Ej: http://orders-service/api
        """
        self.base_url = base_url.rstrip("/") if base_url else ""

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}" if self.base_url else endpoint

    def get(self, endpoint: str):
        url = self._build_url(endpoint)
        headers = self._auth_header()

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            return response.json()
        
        except Timeout:
            logger.error(f"⏳ Timeout al llamar GET {url}")
            return {"error": "El servicio tardó demasiado en responder"}

        except HTTPError as err:
            logger.error(f"❌ Error HTTP en GET {url}: {err}")
            return {"error": f"Error en el microservicio: {err}"}

        except ConnectionError:
            logger.error(f"🔌 No se pudo conectar con {url}")
            return {"error": "No hay conexión con el microservicio"}

        except Exception as e:
            logger.error(f"⚠ Error inesperado en GET {url}: {str(e)}")
            return {"error": "Ha ocurrido un error inesperado"}

    def post(self, endpoint: str, data: dict):
        url = self._build_url(endpoint)
        headers = self._auth_header()

        try:
            response = requests.post(url, json=data, headers=headers, timeout=5)
            response.raise_for_status()
            return response.json()

        except Timeout:
            logger.error(f"⏳ Timeout al llamar POST {url}")
            return {"error": "El servicio tardó demasiado en responder"}

        except HTTPError as err:
            logger.error(f"❌ Error HTTP en POST {url}: {err}")
            return {"error": f"Error en el microservicio: {err}"}

        except ConnectionError:
            logger.error(f"🔌 No se pudo conectar con {url}")
            return {"error": "No hay conexión con el microservicio"}

        except Exception as e:
            logger.error(f"⚠ Error inesperado en POST {url}: {str(e)}")
            return {"error": "Ha ocurrido un error inesperado"}

    def _auth_header(self):
        return {"Authorization": f"Bearer {session.token}"} if session.token else {}
