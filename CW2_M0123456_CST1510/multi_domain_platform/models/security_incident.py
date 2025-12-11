class SecurityIncident:
    def __init__(
        self,
        incident_id: int,
        date: str,
        incident_type: str,
        severity: str,
        status: str,
        description: str,
    ):
        self.id = incident_id
        self.date = date
        self.incident_type = incident_type
        self.severity = severity
        self.status = status
        self.description = description

    def is_critical(self) -> bool:
        return self.severity.upper() == "CRITICAL"
