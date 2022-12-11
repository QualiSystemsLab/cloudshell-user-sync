"""
https://github.com/dbader/schedule
"""
import logging

import schedule
import time
from cloudshell_user_sync.ldap_sync import run_ldap_sync


def ldap_sync_job(config_path, logger):
    run_ldap_sync(json_config_path=config_path, logger=logger)


class ScheduleHandler:
    def __init__(self, config_path: str, logger: logging.Logger, frequency_seconds: int = 120):
        self.frequency_seconds = frequency_seconds
        self.logger = logger
        self.config_path = config_path
        self.active = False

    def run_scheduler(self):
        self.logger.info("Starting Cloudshell Sync Service")
        schedule.every(self.frequency_seconds).seconds.do(ldap_sync_job,
                                                          config_path=self.config_path,
                                                          logger=self.logger)
        self.active = True
        while self.active:
            schedule.run_pending()
            time.sleep(1)

    def stop_scheduler(self):
        self.logger.info("Stopping Cloudshell Sync Service")
        self.active = False
        schedule.clear()
