import platform
import sys

import click

from cloudshell_user_sync.utility.windows_service import CloudshellSyncWinService


def run_service_flow():
    curr_platform = platform.system().lower()
    if curr_platform == "windows":
        click.echo("Starting Windows Service")
        sys.argv.pop(1)
        click.echo(f"{sys.argv}")
        CloudshellSyncWinService.parse_command_line()
    elif curr_platform == "linux":
        raise NotImplementedError("Linux service generation command not supported")
    else:
        raise ValueError(f"Unknown platform: {curr_platform}")
    click.secho("Service Command Completed", fg="yellow")
