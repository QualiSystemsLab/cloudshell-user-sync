import pytest
from cloudshell.api.cloudshell_api import CloudShellAPISession
from logger_stdout import get_logger
import env_settings
from cloudshell_user_sync.utility.ldap3_handler import Ldap3Handler


@pytest.fixture(scope="session")
def cs_api() -> CloudShellAPISession:
    return CloudShellAPISession(env_settings.CS_SERVER,
                                env_settings.CS_ADMIN_USER,
                                env_settings.CS_ADMIN_PASSWORD,
                                env_settings.CS_DOMAIN)


@pytest.fixture(scope="session")
def ldap_handler() -> Ldap3Handler:
    return Ldap3Handler(server=env_settings.LDAP_SERVER,
                        user_cn=env_settings.LDAP_USER,
                        password=env_settings.LDAP_PASSWORD,
                        base_dn=env_settings.LDAP_BASE_DN)


@pytest.fixture(scope="session")
def std_out_logger() -> CloudShellAPISession:
    return get_logger("test logger")
