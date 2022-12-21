"""
Sanity check that config files read correctly
"""
from cloudshell_user_sync.utility import config_handler

def test_ldap_config_handler(ldap_config):
    print("\nReading config...")
    ldap_server = ldap_config.ldap_details.server
    assert ldap_server
    print(f"LDAP Server: {ldap_server}")


def test_generate_config_handler():
    config_handler.generate_sync_config_to_path()