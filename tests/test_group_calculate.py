from typing import List

from cloudshell_user_sync.actions import cloudshell_sync
import pytest
from cloudshell_user_sync.models.cs_import import ImportGroupData
from unittest.mock import MagicMock


def generate_mock_cs_group(group_name, users: List[str]):
    group1_mock = MagicMock()
    group1_mock.Name = group_name
    group1_mock.Users = []
    for user in users:
        mock_user = MagicMock()
        mock_user.Name = user
        group1_mock.Users.append(mock_user)
    return group1_mock


@pytest.fixture(scope="module")
def import_data() -> List[ImportGroupData]:
    data_list = [
        ImportGroupData(ldap_group_cn="AD Users",
                        target_cloudshell_groups=["SE"],
                        users=["user1", "user3"])
    ]
    return data_list


@pytest.fixture(scope="module")
def cs_db_groups() -> cloudshell_sync.CloudshellGroupInfoMap:
    """ cloudshell group name mapped to GroupInfo"""
    return {
        "QA": generate_mock_cs_group("QA", ["user1", "user2"]),
        "SE": generate_mock_cs_group("SE", ["user3", "user4"]),
        "DEV": generate_mock_cs_group("DEV", ["user5", "user6"])
    }


@pytest.fixture(scope="module")
def cs_users_set() -> cloudshell_sync.CloudshellGroupInfoMap:
    """ cloudshell group name mapped to GroupInfo"""
    return {"user1", "user2", "user3", "user4", "user5", "user6"}


def test_calculate_groups(import_data, cs_db_groups, cs_users_set):
    to_add_table, to_remove_table = cloudshell_sync.calculate_groups_to_add_and_delete(import_data_list=import_data,
                                                                                       cs_db_groups=cs_db_groups,
                                                                                       all_cs_users_set=cs_users_set)
    assert "user1" in to_add_table["SE"]
    assert "user4" in to_remove_table["SE"]
