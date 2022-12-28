from cloudshell_user_sync.utility import config_handler, path_helper, safe_echo
from cloudshell_user_sync.utility.rotating_log_handler import get_rotating_logger
from cloudshell_user_sync.utility.schedule_handler import ScheduleHandler


def run_scheduled_jobs():
    logger = get_rotating_logger()
    config_path = path_helper.get_system_config_path()
    sync_config = config_handler.get_sync_config(config_path, logger)
    config_handler.validate_config(sync_config)
    logger.setLevel(sync_config.service_config.log_level)
    schedule_handler = ScheduleHandler()
    safe_echo.safe_echo("Starting Scheduler")
    schedule_handler.run_scheduler()
