class User:
    def __init__(self, username: str, role: str, email: str | None = None):
        self.username = username
        self.role = role
        self.email = email

    def is_admin(self) -> bool:
        return self.role.lower() == "admin"
