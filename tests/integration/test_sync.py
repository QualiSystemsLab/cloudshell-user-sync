"""
integration test
"""
from cloudshell_user_sync.commands.sync_groups import sync_groups_flow


def test_sync():
    sync_groups_flow()
    pass
