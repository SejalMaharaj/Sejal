class ITTicket:
    def __init__(
        self,
        ticket_id: int,
        priority: str,
        subject: str,
        status: str,
        category: str,
    ):
        self.id = ticket_id
        self.priority = priority
        self.subject = subject
        self.status = status
        self.category = category

    def is_open(self) -> bool:
        return self.status.lower() in {"open", "in progress"}
