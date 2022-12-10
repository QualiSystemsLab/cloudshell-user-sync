"""
"Inbound" groups is the user data coming from external data source like LDAP / AD
"""
import logging
from typing import List, Dict

from cloudshell.api.cloudshell_api import CloudShellAPISession, GroupInfo
from cloudshell_user_sync.models import cs_import


class SyncInboundGroupsAction:
    def __init__(self, api: CloudShellAPISession, inbound_groups_data: List[cs_import.InboundGroupData], logger: logging.Logger):
        self._api = api
        self._logger = logger
        self._inbound_groups_data = inbound_groups_data
        self._cs_db_groups = self._get_cs_groups_dict()
        self._all_cs_users_set = self._get_all_cs_users_set()
        self._validate_inbound_groups()

    def _get_cs_groups_dict(self) -> dict[str, GroupInfo]:
        all_cloudshell_groups = self._api.GetGroupsDetails().Groups
        return {group.Name: group for group in all_cloudshell_groups}

    def _get_all_cs_users_set(self) -> List[str]:
        all_users = self._api.GetAllUsersDetails().Users
        return {x.Name for x in all_users}

    def _validate_inbound_groups(self):
        missing_groups_set = set()
        for curr_data in self._inbound_groups_data:
            for group in curr_data.target_cloudshell_groups:
                if group not in self._cs_db_groups:
                    missing_groups_set.add(group)
        if missing_groups_set:
            err_msg = f"The following groups in config do not exist: {list(missing_groups_set)}"
            self._logger.error(err_msg)
            raise ValueError(err_msg)

    def sync_inbound_groups(self):
        """
        The logic is to sync existing cloudshell users to their respective groups in LDAP / AD
        Users must log in first once manually to have their user imported. Non-imported users are not synced.
        """
        to_add_table: Dict[str, List[str]] = {}
        to_remove_table: Dict[str, List[str]] = {}
        for inbound_group_data in self._inbound_groups_data:
            for group in inbound_group_data.target_cloudshell_groups:
                inbound_users_set = set(inbound_group_data.inbound_users)

                # here we check if the external users first exist in cloudshell
                valid_inbound_users = inbound_users_set.intersection(self._all_cs_users_set)
                cs_db_group_users = self._cs_db_groups[group].Users
                cs_db_group_users_set = {x.Name for x in cs_db_group_users}

                # start set comparisons, and append to group hash tables
                to_add = valid_inbound_users - cs_db_group_users_set
                to_remove = cs_db_group_users_set - valid_inbound_users
                if to_add:
                    to_add_set = to_add_table.get(group, set())
                    to_add_set.update(to_add)
                    to_add_table[group] = to_add_set
                if to_remove:
                    to_remove_set = to_remove_table.get(group, set())
                    to_remove_set.update(to_remove)
                    to_remove_table[group] = to_remove_set

        if to_add_table:
            for group in to_add_table:
                users_list = list(to_add_table[group])
                self._logger.info(f"Adding users to group: {group}\n{users_list}")
                self._api.AddUsersToGroup(users_list, group)

        if to_remove_table:
            for group in to_remove_table:
                users_list = list(to_remove_table[group])
                self._logger.info(f"Removing users from group: {group}\n{users_list}")
                self._api.RemoveUsersFromGroup(users_list, group)
