"""
read in JSON config and generate config data objects
https://stackoverflow.com/a/53713336
"""
import json
import logging
from pathlib import Path

from cloudshell.api.cloudshell_api import CloudShellAPISession

from cloudshell_user_sync import exceptions
from cloudshell_user_sync.models import config
from cloudshell_user_sync.utility import keyring_handler
from cloudshell_user_sync.utility.ldap3_handler import Ldap3Handler
from cloudshell_user_sync.utility import path_helper
import dacite
from dataclasses import asdict
import os


def get_empty_config() -> config.SyncConfig:
    return config.SyncConfig(cloudshell_details=config.CloudshellDetails(),
                             ldap_details=config.LdapDetails(),
                             ldap_mappings=[],
                             service_config=config.ServiceConfig())


def write_sync_config(config_path: str, sync_config: config.SyncConfig):
    """ generate new config"""
    output_file = Path(config_path)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    config_dict = asdict(sync_config)
    with open(config_path, "w+") as f:
        f.write(json.dumps(config_dict, indent=4))


def get_sync_config_from_json(config_path: str, logger: logging.Logger) -> config.SyncConfig:
    # find the config file

    if not os.path.isfile(config_path):
        default_config = get_empty_config()
        write_sync_config(config_path, default_config)
        return default_config

    try:
        with open(config_path) as f:
            data = json.load(f)
    except Exception as e:
        err_msg = f"Issue opening file at path: {config_path}. {type(e).__name__}: {str(e)}"
        logger.error(err_msg)
        raise exceptions.ConfigLoadError(err_msg)

    # load the config object
    try:
        sync_config = dacite.from_dict(data_class=config.SyncConfig, data=data)
    except Exception as e:
        err_msg = f"Issue loading config data object: {type(e).__name__}: {str(e)}"
        logger.error(err_msg)
        raise exceptions.ConfigLoadError(err_msg)

    return sync_config


def get_sync_config(logger: logging.Logger) -> config.SyncConfig:
    config_path = path_helper.get_system_config_path()
    sync_config = get_sync_config_from_json(config_path, logger)
    cs_creds = keyring_handler.get_cs_creds()
    ldap_creds = keyring_handler.get_cs_creds()
    if cs_creds:
        sync_config.cloudshell_details.user = cs_creds.username
        sync_config.cloudshell_details.password = cs_creds.password
    if ldap_creds:
        sync_config.ldap_details.user = ldap_creds.username
        sync_config.ldap_details.password = ldap_creds.password
    return sync_config


def set_cs_credentials(user: str, password: str, logger: logging.Logger):
    logger.info(f"setting cloudshell credentials for user: {user}")
    config_path = path_helper.get_system_config_path()

    # update credential manager
    keyring_handler.set_cloudshell_keyring(user, password)

    # update config file
    sync_config = get_sync_config_from_json(config_path, logger)
    sync_config.cloudshell_details.user = user
    sync_config.cloudshell_details.password = config.SET
    write_sync_config(config_path, sync_config)


def set_ldap_credentials(user: str, password: str, logger: logging.Logger):
    logger.info(f"setting ldap credentials for user: {user}")
    config_path = path_helper.get_system_config_path()

    # update credential manager
    keyring_handler.set_ldap_keyring(user, password)

    # update config file
    sync_config = get_sync_config_from_json(config_path, logger)
    sync_config.ldap_details.user = user
    sync_config.ldap_details.password = config.SET
    write_sync_config(config_path, sync_config)


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
                        user_cn=ldap_details.user,
                        password=ldap_details.password,
                        base_dn=ldap_details.base_dn)
