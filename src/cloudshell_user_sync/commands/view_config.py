import json

from cloudshell_user_sync.utility import config_handler
from cloudshell_user_sync.utility.rotating_log_handler import get_rotating_logger
from cloudshell_user_sync.utility import path_helper
import click


def view_config_json():
    logger = get_rotating_logger()
    config_path = path_helper.get_system_config_path()
    click.echo(f"config path: {config_path}")
    sync_config = config_handler.get_sync_config(logger)
    click.echo(json.dumps(sync_config, indent=4))