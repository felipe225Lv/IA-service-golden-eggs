class SessionState:
    def __init__(self):
        self.token = None
        self.user = None
        
        # Conversación guiada
        self.is_registering = False
        self.registration_data = {}
        self.pending_field = None

        self.pending_action = None
        
        self.memory = {}
session = SessionState()
