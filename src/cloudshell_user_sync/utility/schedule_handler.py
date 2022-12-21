"""
https://github.com/dbader/schedule
"""
import schedule
import time
from cloudshell_user_sync.commands.sync_groups import sync_groups_flow
from cloudshell_user_sync.utility import config_handler
from cloudshell_user_sync.utility.rotating_log_handler import get_rotating_logger


def ldap_sync_job():
    sync_groups_flow()


class ScheduleHandler:
    def __init__(self):
        self.logger = get_rotating_logger()
        self.sync_config = config_handler.get_sync_config(self.logger)
        self.logger.setLevel(self.sync_config.service_config.log_level)
        self.frequency = self.sync_config.service_config.job_frequency_seconds
        self.active = False

    def run_scheduler(self):
        self.logger.info("Starting Cloudshell Sync Service")
        schedule.every(self.frequency).seconds.do(ldap_sync_job)
        self.active = True
        while self.active:
            schedule.run_pending()
            time.sleep(1)

    def stop_scheduler(self):
        self.logger.info("Stopping Cloudshell Sync Service")
        self.active = False
        schedule.clear()
