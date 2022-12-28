from _pytest.fixtures import fixture

from cloudshell_user_sync.models import config
from cloudshell_user_sync.utility import config_handler


@fixture
def config_path():
    return "ldap_config.json"


def test_config_from_json(config_path, std_out_logger):
    sync_config = config_handler.get_sync_config_from_json(config_path, std_out_logger)
    assert isinstance(sync_config, config.SyncConfig)


def test_get_config(config_path, std_out_logger):
    sync_config = config_handler.get_sync_config(config_path, std_out_logger)
    assert isinstance(sync_config, config.SyncConfig)


def test_set_mapping(config_path, std_out_logger):
    config_handler.set_ldap_mapping(config_path, "test_dn", ["csgroup1", "csgroup2"], std_out_logger)


def test_set_kv_pair(config_path, std_out_logger):
    config_handler.set_config_kv_pair(config_path, "cloudshell", "server", "1.1.1.1", std_out_logger)


def test_set_credential(config_path, std_out_logger):
    ldap_user, ldap_password = "Administrator", "Password123!"
    cs_user, cs_password = "admin", "admin"
    config_handler.set_ldap_credentials(ldap_user, ldap_password, std_out_logger)
    config_handler.set_cs_credentials(cs_user, cs_password, std_out_logger)
    config = config_handler.get_sync_config(config_path, std_out_logger)
    assert config.ldap_details.user_dn == ldap_user
    assert config.ldap_details.password == ldap_password
    assert config.cloudshell_details.user == cs_user
    assert config.cloudshell_details.password == cs_password
