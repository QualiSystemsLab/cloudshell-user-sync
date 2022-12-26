from cloudshell_user_sync import exceptions
from cloudshell_user_sync.actions import cloudshell_sync
from cloudshell_user_sync.models import config
from cloudshell_user_sync.utility import config_handler
from cloudshell_user_sync.utility.rotating_log_handler import get_rotating_logger


def sync_groups_flow():
    # read in sync config
    logger = get_rotating_logger()
    sync_config = config_handler.get_sync_config(logger)

    if sync_config.cloudshell_details.user == config.UNSET:
        raise exceptions.FatalError("Set Cloudshell Credentials Before Running")

    if sync_config.ldap_details.user_dn == config.UNSET:
        raise exceptions.FatalError("Set LDAP Credentials Before Running")

    if not sync_config.ldap_mappings:
        raise exceptions.FatalError("No LDAP Group Mappings Defined in Config")

    logger.setLevel(sync_config.service_config.log_level)
    api = config_handler.get_api_from_cs_config(cs_config=sync_config.cloudshell_details, logger=logger)
    ldap_handler = config_handler.get_ldap_handler_from_config(ldap_details=sync_config.ldap_details)

    # run ldap sync action
    cloudshell_sync.ldap_pull_cloudshell_sync(
        api=api, ldap_handler=ldap_handler, ldap_mappings=sync_config.ldap_mappings, logger=logger
    )
