import pytest
from cloudshell.api.cloudshell_api import CloudShellAPISession
from logger_stdout import get_logger
from cloudshell_user_sync.models import ldap_config
from cloudshell_user_sync import config_handler


@pytest.fixture(scope="session")
def cs_api() -> CloudShellAPISession:
    return CloudShellAPISession("localhost", "admin", "admin", "Global")


@pytest.fixture(scope="session")
def ldap_config() -> ldap_config.LdapConfig:
    return config_handler.get_ldap_config_from_json("sample_ldap_config.json")


@pytest.fixture(scope="session")
def std_out_logger() -> CloudShellAPISession:
    return get_logger("test logger")
