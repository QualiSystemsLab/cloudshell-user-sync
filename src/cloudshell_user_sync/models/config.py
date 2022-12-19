from dataclasses import dataclass
from typing import List


@dataclass
class CloudshellDetails:
    user: str
    password: str
    server: str = "localhost"
    domain: str = "Global"


@dataclass
class LdapDetails:
    user_cn: str
    password: str
    server: str = "localhost"
    base_dn: str = "DC=corp,DC=example,DC=com"


@dataclass
class LdapGroupsMapping:
    ldap_cn: str
    cloudshell_groups: List[str]


@dataclass
class ServiceConfig:
    job_frequency_seconds: int = 120


# this represents the user json structure, to be combined with keyring credential data
@dataclass
class UserJsonConfig:
    cs_server: str
    ldap_server: str
    ldap_mappings: List[LdapGroupsMapping]
    service_config: ServiceConfig
    ldap_base_dn: str = "DC=corp,DC=example,DC=com"


# this is internal data model
@dataclass
class SyncConfig:
    cloudshell_details: CloudshellDetails
    ldap_details: LdapDetails
    ldap_mappings: List[LdapGroupsMapping]
    service_config: ServiceConfig
