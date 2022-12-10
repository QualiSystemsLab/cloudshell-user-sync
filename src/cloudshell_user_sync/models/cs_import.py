from dataclasses import dataclass
from typing import List, Optional


@dataclass
class InboundGroupData:
    external_group_uid: str
    target_cloudshell_groups: List[str]
    inbound_users: List[str]


@dataclass
class CloudshellUserData:
    name: str
    email: Optional[str]
    password: Optional[str]
