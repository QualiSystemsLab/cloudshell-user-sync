import json
from dataclasses import asdict

import click

from cloudshell_user_sync import exceptions
from cloudshell_user_sync.utility import config_handler, path_helper
from cloudshell_user_sync.utility.rotating_log_handler import get_rotating_logger


def view_or_set_config(target: str, key: str, value: str):
    """
    If all params passed add new key
    If no params passed show current config
    If partial params passed throw validation error
    """
    logger = get_rotating_logger()
    config_path = path_helper.get_system_config_path()
    passed_params = [target, key, value]
    if all(passed_params):
        click.echo(f"Setting '{target}' config. Key: {key}, Value: {value}")
        config_handler.set_config_kv_pair(target, key, value, logger)
        click.secho("Config Value Set", fg="green")
    elif any(passed_params):
        exc_msg = f"Invalid Set Config Params passed. Target: {target}, Key: {key}, Value: {value}"
        raise exceptions.FatalError(exc_msg)
    else:
        click.echo(f"Config Path: {config_path}")
        sync_config = config_handler.get_sync_config_from_json(config_path, logger)
        click.echo(json.dumps(asdict(sync_config), indent=4))
