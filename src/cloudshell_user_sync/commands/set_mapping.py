import json
from dataclasses import asdict
import click

from cloudshell_user_sync.utility import config_handler
from cloudshell_user_sync.utility.rotating_log_handler import get_rotating_logger


def set_ldap_mapping(ldap_cn: str, cloudshell_groups: str):
    """
    cloudshell groups is comma separated string from cli, convert to list here
    """
    logger = get_rotating_logger()
    cs_groups = [x.strip() for x in cloudshell_groups.split(",")]
    config_handler.set_ldap_mapping(ldap_cn=ldap_cn, cloudshell_groups=cs_groups, logger=logger)


def delete_ldap_mapping(ldap_cn: str):
    logger = get_rotating_logger()
    config_handler.delete_ldap_mapping(ldap_cn, logger)


def view_mappings():
    logger = get_rotating_logger()
    mappings = config_handler.get_mappings_config(logger)
    dict_list = [asdict(x) for x in mappings]
    click.echo(json.dumps(dict_list, indent=4))
