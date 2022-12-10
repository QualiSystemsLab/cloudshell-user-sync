"""
read in JSON config and generate config data objects
https://stackoverflow.com/a/53713336
"""
import json
import logging

from cloudshell.api.cloudshell_api import CloudShellAPISession

from cloudshell_user_sync import exceptions
from cloudshell_user_sync.models import ldap_config, cs_config
import dacite


def get_ldap_config_from_json(json_path: str) -> ldap_config.LdapConfig:
    with open(json_path) as f:
        data = json.load(f)
    config = dacite.from_dict(data_class=ldap_config.LdapConfig, data=data)
    return config


def get_api_from_cs_config(config: cs_config.CloudshellDetails, logger: logging.Logger) -> CloudShellAPISession:
    try:
        api = CloudShellAPISession(config.server, config.user, config.password, config.domain)
    except Exception as e:
        err_msg = f"Issue instantiating api session. {str(e)}"
        logger.error(err_msg)
        raise exceptions.CloudshellApiException(err_msg)
    return api
