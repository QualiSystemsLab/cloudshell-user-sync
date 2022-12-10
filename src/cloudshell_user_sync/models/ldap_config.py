from dataclasses import dataclass
from typing import List
from cloudshell_user_sync.models.cs_config import CloudshellDetails


@dataclass
class LdapDetails:
    server: str
    user_dn: str
    password: str
    search_base: str


@dataclass
class LdapMapping:
    ldap_dn: str
    cloudshell_groups: List[str]


@dataclass
class LdapConfig:
    cloudshell_details: CloudshellDetails
    ldap_details: LdapDetails
    ldap_mappings: List[LdapMapping]
