from cloudshell_user_sync.utility import config_handler
from cloudshell_user_sync.utility.rotating_log_handler import get_rotating_logger


def set_credentials(user: str, password: str, target_service: str):
    logger = get_rotating_logger()

    if target_service.lower() in ["cloudshell", "cs"]:
        config_handler.set_cs_credentials(user, password, logger)
    elif target_service.lower() == "ldap":
        config_handler.set_ldap_credentials(user, password, logger)

    raise ValueError(f"target service type {target_service} not valid")