"""
read in JSON config and generate config data objects
https://stackoverflow.com/a/53713336
"""
import json
import logging
import os
from dataclasses import asdict
from pathlib import Path
from typing import List

import dacite
from cloudshell.api.cloudshell_api import CloudShellAPISession

from cloudshell_user_sync import exceptions
from cloudshell_user_sync.models import config
from cloudshell_user_sync.utility import keyring_handler
from cloudshell_user_sync.utility.ldap3_handler import Ldap3Handler


def get_empty_config() -> config.SyncConfig:
    return config.SyncConfig(
        cloudshell_details=config.CloudshellDetails(),
        ldap_details=config.LdapDetails(),
        ldap_mappings=[],
        service_config=config.ServiceConfig(),
    )


def write_sync_config(config_path: str, sync_config: config.SyncConfig):
    """
    dump config as json to file
    remove the ldap / cloudshell credentials before dumping as they are managed in credential manager
    """
    output_file = Path(config_path)

    # make missing folders on first write
    output_file.parent.mkdir(exist_ok=True, parents=True)

    config_dict = asdict(sync_config)

    # remove credentials before dumping
    del config_dict["cloudshell_details"]["user"]
    del config_dict["cloudshell_details"]["password"]
    del config_dict["ldap_details"]["user_dn"]
    del config_dict["ldap_details"]["password"]

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


def get_sync_config(config_path: str, logger: logging.Logger) -> config.SyncConfig:
    sync_config = get_sync_config_from_json(config_path, logger)
    cs_creds = keyring_handler.get_cs_creds()
    ldap_creds = keyring_handler.get_ldap_creds()
    if cs_creds:
        sync_config.cloudshell_details.user = cs_creds.username
        sync_config.cloudshell_details.password = cs_creds.password
    if ldap_creds:
        sync_config.ldap_details.user_dn = ldap_creds.username
        sync_config.ldap_details.password = ldap_creds.password
    return sync_config


def set_cs_credentials(user: str, password: str, logger: logging.Logger):
    logger.info(f"setting cloudshell credentials for user: {user}")
    keyring_handler.set_cloudshell_keyring(user, password)


def set_ldap_credentials(user: str, password: str, logger: logging.Logger):
    logger.info(f"setting ldap credentials for user: {user}")
    keyring_handler.set_ldap_keyring(user, password)


def set_ldap_mapping(config_path: str, ldap_dn: str, cloudshell_groups: List[str], logger: logging.Logger):
    sync_config = get_sync_config_from_json(config_path, logger)
    curr_mappings = sync_config.ldap_mappings
    new_mapping = config.LdapGroupsMapping(ldap_dn, cloudshell_groups)
    dn_list = [x.ldap_dn for x in curr_mappings]
    logger.info(f"setting ldap mapping. LDAP DN: {ldap_dn}, CS Groups: {cloudshell_groups}")
    if ldap_dn in dn_list:
        existing_index = dn_list.index(ldap_dn)
        curr_mappings[existing_index] = new_mapping
    else:
        curr_mappings.append(new_mapping)
    write_sync_config(config_path, sync_config)


def delete_ldap_mapping(config_path: str, ldap_dn: str, logger: logging.Logger):
    sync_config = get_sync_config_from_json(config_path, logger)
    curr_mappings = sync_config.ldap_mappings
    dn_list = [x.ldap_dn for x in curr_mappings]
    if ldap_dn in dn_list:
        logger.info(f"deleting ldap mapping. LDAP DN: {ldap_dn}")
        existing_index = dn_list.index(ldap_dn)
        curr_mappings.pop(existing_index)
        write_sync_config(config_path, sync_config)


def get_mappings_config(config_path: str, logger: logging.Logger) -> List[config.LdapGroupsMapping]:
    sync_config = get_sync_config_from_json(config_path, logger)
    return sync_config.ldap_mappings


def set_config_kv_pair(config_path: str, target: str, key: str, value: str, logger: logging.Logger):
    def validate_key(target_obj, config_key):
        try:
            getattr(target_obj, config_key)
        except AttributeError:
            raise exceptions.FatalError(f"{config_key} not present in {target} config")

    sync_config = get_sync_config_from_json(config_path, logger)
    if target.lower() == "ldap":
        ldap_config = sync_config.ldap_details
        validate_key(ldap_config, key)
        setattr(ldap_config, key, value)
    elif target.lower() in ["cs", "cloudshell"]:
        cs_config = sync_config.cloudshell_details
        validate_key(cs_config, key)
        setattr(cs_config, key, value)
    elif target.lower() == "service":
        service_config = sync_config.service_config
        validate_key(service_config, key)
        if key == "job_frequency_seconds":
            try:
                value = int(value)
            except ValueError:
                raise exceptions.FatalError(f"'{key}' must be of int type. Got '{value}'")
        setattr(service_config, key, value)
    else:
        raise exceptions.FatalError(f"invalid target config: {target}")
    logger.info(f"setting {target} key-value pair: {key} - {value}")
    write_sync_config(config_path, sync_config)


def validate_config(sync_config: config.SyncConfig):
    if not sync_config.ldap_details.user_dn or not sync_config.ldap_details.password:
        raise exceptions.FatalError("No LDAP Credentials Set")
    if not sync_config.cloudshell_details.user or not sync_config.cloudshell_details.password:
        raise exceptions.FatalError("No Cloudshell Credentials Set")
    if not sync_config.ldap_mappings:
        raise exceptions.FatalError("No LDAP Group Mappings Defined in Config")


def prep_config_for_display(sync_config: config.SyncConfig) -> config.SyncConfig:
    cs_details = sync_config.cloudshell_details
    ldap_details = sync_config.ldap_details

    if not cs_details.user:
        cs_details.user = config.UNSET

    if cs_details.password:
        cs_details.password = config.SET_PASSWORD
    else:
        cs_details.password = config.UNSET

    if not ldap_details.user_dn:
        ldap_details.user_dn = config.UNSET

    if ldap_details.password:
        ldap_details.password = config.SET_PASSWORD
    else:
        ldap_details.password = config.UNSET

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
    return Ldap3Handler(
        server=ldap_details.server, user_dn=ldap_details.user_dn, password=ldap_details.password, base_dn=ldap_details.base_dn
    )
