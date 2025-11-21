# core/session_state.py

class SessionState:
    def __init__(self):
        self.is_authenticated = False
        self.user_id = None
        self.role = "GUEST"

        # Session memory for tasks
        self.pending_action = None
        self.is_registering = False
        self.registration_data = {}
        self.pending_field = None
        self.token = None

session = SessionState()