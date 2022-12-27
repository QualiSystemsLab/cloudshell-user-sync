import logging
from dataclasses import dataclass
from typing import List

UNSET = "UNSET"
SET_PASSWORD = "************"
DEFAULT_JOB_FREQUENCY_SECONDS = 600  # every ten minutes


@dataclass
class CloudshellDetails:
    user: str = ""
    password: str = ""
    server: str = "localhost"
    domain: str = "Global"


@dataclass
class LdapDetails:
    user_dn: str = ""
    password: str = ""
    server: str = ""
    base_dn: str = ""


@dataclass
class LdapGroupsMapping:
    ldap_dn: str
    cloudshell_groups: List[str]


@dataclass
class ServiceConfig:
    job_frequency_seconds: int = DEFAULT_JOB_FREQUENCY_SECONDS
    log_level: str = logging.getLevelName(logging.INFO)


@dataclass
class SyncConfig:
    service_config: ServiceConfig
    cloudshell_details: CloudshellDetails
    ldap_details: LdapDetails
    ldap_mappings: List[LdapGroupsMapping]
