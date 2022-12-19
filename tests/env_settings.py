"""
create .env file in tests directory with following keys:
CS_ADMIN_USER=admin
CS_ADMIN_PASSWORD=admin
CS_SERVER=localhost
CS_DOMAIN=Global

LDAP_SERVER=ldap://localhost
LDAP_USER=Administrator
LDAP_PASSWORD=Password1
LDAP_BASE_DN=DC=natticorp,DC=example,DC=com
"""

import os
from dotenv import load_dotenv

load_dotenv()

# server credentials from .env
CS_ADMIN_USER = os.environ.get("CS_ADMIN_USER")
CS_ADMIN_PASSWORD = os.environ.get("CS_ADMIN_PASSWORD")
CS_SERVER = os.environ.get("CS_SERVER")
CS_DOMAIN = os.environ.get("CS_DOMAIN")

LDAP_SERVER = os.environ.get("LDAP_SERVER")
LDAP_USER = os.environ.get("LDAP_USER")
LDAP_PASSWORD = os.environ.get("LDAP_PASSWORD")
LDAP_BASE_DN = os.environ.get("LDAP_BASE_DN")

LDAP_TARGET_GROUP_CN = os.environ.get("LDAP_TARGET_GROUP_CN")
CS_TARGET_GROUPS = os.environ.get("CS_TARGET_GROUPS")

