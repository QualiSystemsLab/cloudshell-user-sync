"""
Integration tests against live LDAP Server
"""
import json

import env_settings
import pytest


@pytest.fixture(scope="module")
def target_group_dn() -> str:
    return env_settings.LDAP_TARGET_GROUP_DN


def test_get_all_groups(ldap_handler):
    all_groups = ldap_handler.get_all_groups_entries()
    assert len(all_groups) > 10
    print(f"\ntotal groups found: {len(all_groups)}")


def test_get_custom_groups(ldap_handler):
    custom_groups = ldap_handler.get_custom_group_entries()
    print(f"\ntotal custom groups found: {len(custom_groups)}")


def test_get_custom_group_dn(ldap_handler):
    custom_groups_dn = ldap_handler.get_custom_group_distinguished_names()
    print(f"\n{len(custom_groups_dn)} custom groups found: {json.dumps(custom_groups_dn, indent=4)}")


def test_get_user_data(ldap_handler, target_group_dn):
    users = ldap_handler.get_user_data_for_group_dn(target_group_dn)
    print(f"\nusers found: {len(users)}")
