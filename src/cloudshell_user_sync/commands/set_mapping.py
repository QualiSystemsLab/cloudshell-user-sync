import json
from dataclasses import asdict

import click

from cloudshell_user_sync.utility import config_handler, path_helper
from cloudshell_user_sync.utility.rotating_log_handler import get_rotating_logger


def set_ldap_mapping(ldap_dn: str, cloudshell_groups: str):
    """
    cloudshell groups is comma separated string from cli, convert to list here
    """
    logger = get_rotating_logger()
    config_path = path_helper.get_system_config_path()
    cs_groups = [x.strip() for x in cloudshell_groups.split(",")]
    config_handler.set_ldap_mapping(config_path=config_path, ldap_dn=ldap_dn, cloudshell_groups=cs_groups, logger=logger)


def delete_ldap_mapping(ldap_dn: str):
    logger = get_rotating_logger()
    config_path = path_helper.get_system_config_path()
    config_handler.delete_ldap_mapping(config_path, ldap_dn, logger)


def view_mappings():
    logger = get_rotating_logger()
    config_path = path_helper.get_system_config_path()
    mappings = config_handler.get_mappings_config(config_path, logger)
    dict_list = [asdict(x) for x in mappings]
    click.echo(json.dumps(dict_list, indent=4))
