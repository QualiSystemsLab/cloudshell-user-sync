"""
read in JSON config and generate config data objects
https://stackoverflow.com/a/53713336
"""
import json
import logging

from cloudshell.api.cloudshell_api import CloudShellAPISession

from cloudshell_user_sync import exceptions
from cloudshell_user_sync.models import config
from cloudshell_user_sync.utility import keyring_handler
from cloudshell_user_sync.utility.ldap3_handler import Ldap3Handler
import dacite


def set_sync_config():
    pass


def get_user_json_config(json_path: str, logger: logging.Logger) -> config.UserJsonConfig:
    # find the config file
    try:
        with open(json_path) as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error(f"Config not found at path: {json_path}")
        raise

    # load in the user json config
    try:
        user_json_config = dacite.from_dict(data_class=config.UserJsonConfig, data=data)
    except Exception as e:
        err_msg = f"Issue loading in json to config object: {type(e).__name__}: {str(e)}"
        logger.error(err_msg)
        raise exceptions.ConfigLoadError(err_msg)

    return user_json_config


def get_sync_config(json_path: str, logger: logging.Logger) -> config.SyncConfig:
    user_config = get_user_json_config(json_path, logger)
    cs_creds = keyring_handler.get_cs_creds()
    ldap_creds = keyring_handler.get_cs_creds()
    cloudshell_details = config.CloudshellDetails(user=cs_creds.username,
                                                  password=cs_creds.password,
                                                  server=user_config.cs_server)
    ldap_details = config.LdapDetails(user_cn=ldap_creds.username,
                                      password=ldap_creds.password,
                                      base_dn=user_config.ldap_base_dn)
    sync_config = config.SyncConfig(cloudshell_details=cloudshell_details,
                                    ldap_details=ldap_details,
                                    ldap_mappings=user_config.ldap_mappings,
                                    service_config=user_config.service_config)
    return sync_config


def get_api_from_cs_config(cs_config: config.CloudshellDetails, logger: logging.Logger) -> CloudShellAPISession:
    try:
        api = CloudShellAPISession(cs_config.server, cs_config.user, cs_config.password, cs_config.domain)
    except Exception as e:
        err_msg = f"Issue instantiating api session. {str(e)}"
        logger.error(err_msg)
        raise exceptions.CloudshellApiException(err_msg)
    return api


def get_ldap_handler_from_config(ldap_details: config.LdapDetails) -> Ldap3Handler:
    return Ldap3Handler(server=ldap_details.server,
                        user_cn=ldap_details.user_cn,
                        password=ldap_details.password,
                        base_dn=ldap_details.base_dn)
