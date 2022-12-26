import keyring
from keyring.credentials import Credential

CS_CREDENTIAL_SERVICE = "User Sync Cloudshell Credentials"
LDAP_CREDENTIAL_SERVICE = "User Sync LDAP Credentials"


def _set_keyring_pass(service_name: str, user_name: str, password):
    keyring.set_password(service_name, user_name, password)


def _get_keyring_creds(service_name: str) -> Credential:
    return keyring.get_credential(service_name=service_name, username=None)


def set_cloudshell_keyring(cs_user: str, cs_password: str):
    _set_keyring_pass(service_name=CS_CREDENTIAL_SERVICE, user_name=cs_user, password=cs_password)


def set_ldap_keyring(ldap_user: str, ldap_password: str):
    _set_keyring_pass(service_name=LDAP_CREDENTIAL_SERVICE, user_name=ldap_user, password=ldap_password)


def get_cs_creds():
    return _get_keyring_creds(service_name=CS_CREDENTIAL_SERVICE)


def get_ldap_creds():
    return _get_keyring_creds(service_name=LDAP_CREDENTIAL_SERVICE)
