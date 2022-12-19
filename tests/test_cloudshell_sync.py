from typing import List

from cloudshell_user_sync.actions.cloudshell_sync import SyncGroupsAction
from cloudshell.api.cloudshell_api import CloudShellAPISession
import pytest
from cloudshell_user_sync.models.cs_import import ImportGroupData
import env_settings


@pytest.fixture(scope="module")
def import_data() -> List[ImportGroupData]:
    data = [
        ImportGroupData(ldap_group_cn=env_settings.LDAP_TARGET_GROUP_CN,
                        target_cloudshell_groups=env_settings.CS_TARGET_GROUPS.split(","),
                        users=["devadmin"])
    ]
    return data


def test_sync(cs_api: CloudShellAPISession, import_data, std_out_logger):
    sync_action = SyncGroupsAction(cs_api, import_data, std_out_logger)
    sync_action.sync_groups()
