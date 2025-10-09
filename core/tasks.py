class GetTodaySalesTask:
    def __init__(self, client):
        self.client = client

    def execute(self):
        url = "http://orders-service:8001/api/orders/today-sales"
        response = self.client.get(url)
        return response.get("total_sales", "Información no disponible")


class UnknownTask:
    def execute(self):
        return "No entendí tu solicitud."
