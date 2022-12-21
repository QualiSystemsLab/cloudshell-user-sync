import logging
from dataclasses import dataclass
from typing import List

UNSET = "UNSET"
SET = "SET"


@dataclass
class CloudshellDetails:
    user: str = UNSET
    password: str = UNSET
    server: str = "localhost"
    domain: str = "Global"


@dataclass
class LdapDetails:
    user: str = UNSET
    password: str = UNSET
    server: str = "localhost"
    base_dn: str = "DC=corp,DC=example,DC=com"


@dataclass
class LdapGroupsMapping:
    ldap_cn: str
    cloudshell_groups: List[str]


@dataclass
class ServiceConfig:
    job_frequency_seconds: int = 120
    log_level: str = logging.getLevelName(logging.INFO)


@dataclass
class SyncConfig:
    service_config: ServiceConfig
    cloudshell_details: CloudshellDetails
    ldap_details: LdapDetails
    ldap_mappings: List[LdapGroupsMapping]
