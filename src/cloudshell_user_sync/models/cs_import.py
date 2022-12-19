from dataclasses import dataclass
from typing import List


@dataclass
class ImportGroupData:
    ldap_group_cn: str
    users: List[str]
    target_cloudshell_groups: List[str]