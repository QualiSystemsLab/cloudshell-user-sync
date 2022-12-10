class CloudshellUserSyncBaseException(Exception):
    pass


class CloudshellApiException(CloudshellUserSyncBaseException):
    pass


class LdapHandlerException(CloudshellUserSyncBaseException):
    pass


class CloudshellSyncGroupsException(CloudshellUserSyncBaseException):
    pass

