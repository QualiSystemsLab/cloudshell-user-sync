"""
define path for windows and linux config files and logs

Windows:
C:/ProgramData/CloudshellUserSync/Logs/UserSync.log
C:/ProgramData/CloudshellUserSync/ldap_config.json

Linux:
/var/log/CloudshellUserSync/Logs/UserSync.log
/opt/CloudshellUserSync/ldap_config.json
"""
import os
import platform

APP_FOLDER = "CloudshellUserSync"
LOG_FOLDER_NAME = "Logs"
LOG_FILE_NAME = "UserSync.log"

LINUX_BASE_LOG_DIR = "/var/log"
LINUX_BASE_CONFIG_DIR = "/opt"

CONFIG_FILE = "ldap_config.json"


def get_windows_log_path():
    return os.path.join(os.getenv("PROGRAMDATA"), APP_FOLDER, LOG_FOLDER_NAME, LOG_FILE_NAME)


def get_windows_config_path():
    return os.path.join(os.getenv("PROGRAMDATA"), APP_FOLDER, CONFIG_FILE)


def get_linux_log_path():
    return os.path.join(LINUX_BASE_LOG_DIR, APP_FOLDER, LOG_FOLDER_NAME, LOG_FILE_NAME)


def get_linux_config_path():
    return os.path.join(LINUX_BASE_CONFIG_DIR, APP_FOLDER, CONFIG_FILE)


def get_system_log_path():
    curr_platform = platform.system().lower()
    if curr_platform == "windows":
        return get_windows_log_path()

    if curr_platform == "linux":
        return get_linux_log_path()

    raise ValueError(f"Unknown platform: {curr_platform}")


def get_system_config_path():
    curr_platform = platform.system().lower()
    if curr_platform == "windows":
        return get_windows_config_path()

    if curr_platform == "linux":
        return get_linux_config_path()

    raise ValueError(f"Unknown platform: {curr_platform}")
