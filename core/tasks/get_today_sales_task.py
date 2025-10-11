class GetTodaySalesTask:
    def __init__(self, client=None):
        self.client = client  # lo dejamos por compatibilidad, aunque no se usa

    def execute(self):
        # Datos simulados (quemados)
        fake_response = {
            "date": "2025-10-11",
            "total_sales": 1520,
            "total_orders": 37,
            "top_products": [
                {"name": "Huevos AA", "quantity": 450, "revenue": 720},
                {"name": "Huevos A", "quantity": 300, "revenue": 480},
                {"name": "Huevos AAA", "quantity": 200, "revenue": 320}
            ],
            "best_seller": {
                "product": "Huevos AA",
                "percentage": "47%"
            }
        }

        # Puedes ajustar el formato de retorno según lo que la IA espera procesar
        return fake_response
