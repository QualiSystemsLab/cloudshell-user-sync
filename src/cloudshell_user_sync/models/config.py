from dataclasses import dataclass
from typing import List


@dataclass
class CloudshellDetails:
    server: str
    user: str
    password: str
    domain: str


@dataclass
class LdapDetails:
    server: str
    user_cn: str
    password: str
    base_dn: str


@dataclass
class LdapGroupsMapping:
    ldap_cn: str
    cloudshell_groups: List[str]


# this represents the user json structure, to be combined with keyring credential data
@dataclass
class UserJsonConfig:
    cs_server: str
    ldap_server: str
    ldap_mappings: List[LdapGroupsMapping]


# this is internal data model
@dataclass
class SyncConfig:
    cloudshell_details: CloudshellDetails
    ldap_details: LdapDetails
    ldap_mappings: List[LdapGroupsMapping]
