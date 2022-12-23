"""
Sanity check that config files read correctly
"""
from cloudshell_user_sync.utility import config_handler
from cloudshell_user_sync.models.config import SyncConfig


def test_get_sync_config(std_out_logger):
    config = config_handler.get_sync_config(std_out_logger)
    assert isinstance(config, SyncConfig)


def test_set_credential(std_out_logger):
    ldap_user, ldap_password = "Administrator", "Password123!"
    cs_user, cs_password = "admin", "admin"
    config_handler.set_ldap_credentials(ldap_user, ldap_password, std_out_logger)
    config_handler.set_cs_credentials(cs_user, cs_password, std_out_logger)
    config = config_handler.get_sync_config(std_out_logger)
    assert config.ldap_details.user == ldap_user
    assert config.ldap_details.password == ldap_password
    assert config.cloudshell_details.user == cs_user
    assert config.cloudshell_details.password == cs_password


def test_set_mapping(std_out_logger):
    ldap_cn = "AD USERS"
    cs_groups = ["QA", "SE"]
    config_handler.set_ldap_mapping(ldap_cn, cs_groups, std_out_logger)
    config = config_handler.get_sync_config(std_out_logger)
    mappings = config.ldap_mappings
    assert ldap_cn in [x.ldap_cn for x in mappings]


