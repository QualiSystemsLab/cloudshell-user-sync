from cloudshell_user_sync.utility.windows_service import CloudshellSyncWinService
import click
import platform


def run_service_flow():
    curr_platform = platform.system().lower()
    if curr_platform == "windows":
        click.echo("Starting Windows Service")
        CloudshellSyncWinService.parse_command_line()
    elif curr_platform == "linux":
        raise NotImplementedError("Linux service generation command not supported")
    else:
        raise ValueError(f"Unknown platform: {curr_platform}")
    click.secho("Service Installed", fg="green")
