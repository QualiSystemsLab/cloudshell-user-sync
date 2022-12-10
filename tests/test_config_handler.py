"""
Sanity check that config files read correctly
"""


def test_ldap_config_handler(ldap_config):
    print("\nReading config...")
    ldap_server = ldap_config.ldap_details.server
    assert ldap_server
    print(f"LDAP Server: {ldap_server}")