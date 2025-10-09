import requests
import logging

logger = logging.getLogger(__name__)

def call_microservice(url: str, params=None, method="GET", data=None):
    """
    Llama a un microservicio REST y retorna su respuesta JSON o error.
    """
    try:
        if method == "GET":
            res = requests.get(url, params=params, timeout=5)
        elif method == "POST":
            res = requests.post(url, json=data, timeout=5)
        else:
            raise ValueError("Método HTTP no soportado")

        res.raise_for_status()
        return res.json()
    except Exception as e:
        logger.error(f"Error llamando al microservicio {url}: {e}")
        return {"error": str(e)}
