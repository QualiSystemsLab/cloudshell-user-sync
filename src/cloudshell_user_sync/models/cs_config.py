from dataclasses import dataclass


@dataclass
class CloudshellDetails:
    server: str
    user: str
    password: str
    domain: str
