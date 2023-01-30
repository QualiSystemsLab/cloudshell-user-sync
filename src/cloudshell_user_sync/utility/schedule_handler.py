"""
https://github.com/dbader/schedule
"""
import time

import schedule

from cloudshell_user_sync import exceptions
from cloudshell_user_sync.commands.sync_groups import sync_groups_flow
from cloudshell_user_sync.utility import config_handler, path_helper
from cloudshell_user_sync.utility.rotating_log_handler import get_rotating_logger


class ScheduleHandler:
    MAX_ERRORS = 3

    def __init__(self):
        self.logger = get_rotating_logger()
        config_path = path_helper.get_system_config_path()
        self.sync_config = config_handler.get_sync_config(config_path, self.logger)
        self.logger.setLevel(self.sync_config.service_config.log_level)
        self.frequency = self.sync_config.service_config.job_frequency_seconds
        self.active = False
        self.error_count = 0

    def run_scheduler(self):
        self.logger.info(f"Starting Run Scheduler. Frequency: {self.frequency} seconds.")
        schedule.every(self.frequency).seconds.do(self.ldap_sync_job)
        self.active = True
        while self.active:
            schedule.run_pending()
            time.sleep(1)

    def stop_scheduler(self):
        self.logger.info("Stopping Scheduler")
        self.active = False
        schedule.clear()

    def ldap_sync_job(self):
        """after 3 straight failures, cancel scheduler"""
        try:
            sync_groups_flow()
        except Exception as e:
            self.error_count += 1
            err_msg = (
                f"Issue Running Sync Job. Error Count: {self.error_count}. "
                f"Exception: {type(e).__name__}. Message: {str(e)}"
            )
            if self.error_count == self.MAX_ERRORS:
                self.logger.error("Retry error count reached. Stopping Scheduler")
                self.logger.exception(err_msg)
                raise exceptions.ScheduledJobError(err_msg)
            self.logger.error(err_msg)
        else:
            # reset error count
            self.error_count = 0


if __name__ == "__main__":
    handler = ScheduleHandler()
    handler.run_scheduler()
