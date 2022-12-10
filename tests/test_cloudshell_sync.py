from typing import List

from cloudshell_user_sync.cloudshell_sync import SyncInboundGroupsAction
from cloudshell.api.cloudshell_api import CloudShellAPISession
import pytest
from cloudshell_user_sync.models.cs_import import InboundGroupData


@pytest.fixture(scope="module")
def inbound_data() -> List[InboundGroupData]:
    data = [
        InboundGroupData(external_group_uid="ad_group_A",
                         target_cloudshell_groups=["QA users", "SE users"],
                         inbound_users=["devadmin"])
    ]
    return data


def test_sync(cs_api: CloudShellAPISession, inbound_data, std_out_logger):
    sync_action = SyncInboundGroupsAction(cs_api, inbound_data, std_out_logger)
    sync_action.sync_inbound_groups()
