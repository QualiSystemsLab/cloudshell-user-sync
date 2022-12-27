from cloudshell_user_sync.actions import cloudshell_sync
from cloudshell_user_sync.utility import config_handler, path_helper
from cloudshell_user_sync.utility.rotating_log_handler import get_rotating_logger


def sync_groups_flow():
    logger = get_rotating_logger()
    config_path = path_helper.get_system_config_path()
    sync_config = config_handler.get_sync_config(config_path, logger)
    config_handler.validate_config(sync_config)
    logger.setLevel(sync_config.service_config.log_level)
    api = config_handler.get_api_from_cs_config(cs_config=sync_config.cloudshell_details, logger=logger)
    ldap_handler = config_handler.get_ldap_handler_from_config(ldap_details=sync_config.ldap_details)
    cloudshell_sync.ldap_pull_cloudshell_sync(api=api,
                                              ldap_handler=ldap_handler,
                                              ldap_mappings=sync_config.ldap_mappings,
                                              logger=logger)
