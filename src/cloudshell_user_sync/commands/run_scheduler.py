from cloudshell_user_sync import exceptions
from cloudshell_user_sync.models import config
from cloudshell_user_sync.utility import config_handler, safe_echo
from cloudshell_user_sync.utility.rotating_log_handler import get_rotating_logger
from cloudshell_user_sync.utility.schedule_handler import ScheduleHandler


def run_scheduled_jobs():
    # read in sync config
    logger = get_rotating_logger()
    sync_config = config_handler.get_sync_config(logger)

    if sync_config.cloudshell_details.user == config.UNSET:
        raise exceptions.FatalError("Set Cloudshell Credentials Before Running")

    if sync_config.ldap_details.user_dn == config.UNSET:
        raise exceptions.FatalError("Set LDAP Credentials Before Running")

    if not sync_config.ldap_mappings:
        raise exceptions.FatalError("No LDAP Group Mappings Defined in Config")

    logger.setLevel(sync_config.service_config.log_level)
    schedule_handler = ScheduleHandler()

    safe_echo.safe_echo("Starting Scheduler")

    # run scheduler
    schedule_handler.run_scheduler()
