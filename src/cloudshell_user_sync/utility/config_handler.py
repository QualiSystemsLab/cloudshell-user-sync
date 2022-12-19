"""
read in JSON config and generate config data objects
https://stackoverflow.com/a/53713336
"""
import json
import logging

from cloudshell.api.cloudshell_api import CloudShellAPISession

from cloudshell_user_sync import exceptions
from cloudshell_user_sync.models import config
import dacite


def set_sync_config():
    pass


def get_sync_config(json_path: str, logger: logging.Logger) -> config.SyncConfig:
    try:
        with open(json_path) as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error(f"Config not found at path: {json_path}")
        raise
    try:
        sync_config = dacite.from_dict(data_class=config.SyncConfig, data=data)
    except Exception as e:
        err_msg = f"Issue loading in json to config object: {type(e).__name__}: {str(e)}"
        logger.error(err_msg)
        raise exceptions.ConfigLoadError(err_msg)
    return sync_config


def get_api_from_cs_config(cs_config: config.CloudshellDetails, logger: logging.Logger) -> CloudShellAPISession:
    try:
        api = CloudShellAPISession(cs_config.server, cs_config.user, cs_config.password, cs_config.domain)
    except Exception as e:
        err_msg = f"Issue instantiating api session. {str(e)}"
        logger.error(err_msg)
        raise exceptions.CloudshellApiException(err_msg)
    return api
