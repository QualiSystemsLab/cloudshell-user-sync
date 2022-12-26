import click


class CloudshellUserSyncBaseException(Exception):
    pass


class FatalError(click.ClickException):
    def __init__(self, message):  # pylint: disable=useless-parent-delegation
        super().__init__(message)

    def show(self, file=None):
        click.secho(f"Error: {self.format_message()}", err=True, fg="red")


class CloudshellApiException(CloudshellUserSyncBaseException):
    pass


class LdapHandlerException(CloudshellUserSyncBaseException):
    pass


class CloudshellSyncGroupsException(CloudshellUserSyncBaseException):
    pass


class ConfigLoadError(CloudshellUserSyncBaseException):
    pass
