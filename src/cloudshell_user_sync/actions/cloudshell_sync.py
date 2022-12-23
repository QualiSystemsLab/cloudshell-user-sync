import json
import logging
from dataclasses import asdict
from typing import List, Dict, NewType, Tuple, Set

from cloudshell.api.cloudshell_api import CloudShellAPISession, GroupInfo

from cloudshell_user_sync import exceptions
from cloudshell_user_sync.models.config import LdapGroupsMapping
from cloudshell_user_sync.models.cs_import import ImportGroupData
from cloudshell_user_sync.actions import ldap_pull
from cloudshell_user_sync.utility.ldap3_handler import Ldap3Handler

LdapToCloudshellGroupsMap = NewType("LdapToCloudshellGroupsMap", Dict[str, List[str]])
CloudshellGroupInfoMap = NewType("CloudshellGroupInfoMap", Dict[str, GroupInfo])


def get_cs_groups_dict(api: CloudShellAPISession) -> CloudshellGroupInfoMap:
    all_cloudshell_groups = api.GetGroupsDetails().Groups
    return {group.Name: group for group in all_cloudshell_groups}


def get_all_cs_users_set(api: CloudShellAPISession) -> Set[str]:
    all_users = api.GetAllUsersDetails().Users
    return {x.Name for x in all_users}


def validate_cloudshell_groups(import_data_list: List[ImportGroupData],
                               cs_db_groups: CloudshellGroupInfoMap,
                               logger: logging.Logger):
    missing_groups_set = set()
    for curr_data in import_data_list:
        for group in curr_data.target_cloudshell_groups:
            if group not in cs_db_groups:
                missing_groups_set.add(group)
    if missing_groups_set:
        err_msg = f"The following groups in config do not exist: {list(missing_groups_set)}"
        logger.error(err_msg)
        raise ValueError(err_msg)


def calculate_groups_to_add_and_delete(import_data_list: List[ImportGroupData],
                                       cs_db_groups: CloudshellGroupInfoMap,
                                       all_cs_users_set: Set[str]) -> Tuple[LdapToCloudshellGroupsMap, LdapToCloudshellGroupsMap]:
    """
    Get back a tuple of what to add / remove
    :return:
    """
    to_add_table: LdapToCloudshellGroupsMap = {}
    to_remove_table: LdapToCloudshellGroupsMap = {}
    for curr_data in import_data_list:
        for group in curr_data.target_cloudshell_groups:
            inbound_users_set = set(curr_data.users)

            # here we check if the external users first exist in cloudshell
            valid_inbound_users = inbound_users_set.intersection(all_cs_users_set)
            cs_db_group_users = cs_db_groups[group].Users
            cs_db_group_users_set = {x.Name for x in cs_db_group_users}

            # start set comparisons, and append to group hash tables
            to_add = valid_inbound_users - cs_db_group_users_set
            to_remove = cs_db_group_users_set - valid_inbound_users
            if to_add:
                to_add_set = to_add_table.get(group, set())
                to_add_set.update(to_add)
                to_add_table[group] = list(to_add_set)
            if to_remove:
                to_remove_set = to_remove_table.get(group, set())
                to_remove_set.update(to_remove)
                to_remove_table[group] = list(to_remove_set)
    return to_add_table, to_remove_table


def sync_cloudshell_groups(api: CloudShellAPISession,
                           import_data_list: List[ImportGroupData],
                           logger: logging.Logger):
    # get cloudshell data
    cs_db_groups = get_cs_groups_dict(api)
    all_cs_users = get_all_cs_users_set(api)

    # validate cloudshell groups from config
    validate_cloudshell_groups(import_data_list, cs_db_groups, logger)

    # calculate who is being added / removed from groups
    to_add_map, to_remove_map = calculate_groups_to_add_and_delete(import_data_list, cs_db_groups, all_cs_users)

    if not to_add_map and not to_remove_map:
        logger.debug("No sync action required")

    if to_add_map:
        for group in to_add_map:
            users_list = list(to_add_map[group])
            logger.info(f"Adding users to group: {group}\n{users_list}")
            api.AddUsersToGroup(users_list, group)

    if to_remove_map:
        for group in to_remove_map:
            users_list = list(to_remove_map[group])
            logger.info(f"Removing users from group: {group}\n{users_list}")
            api.RemoveUsersFromGroup(users_list, group)


def ldap_pull_cloudshell_sync(api: CloudShellAPISession,
                              ldap_handler: Ldap3Handler,
                              ldap_mappings: List[LdapGroupsMapping],
                              logger: logging.Logger):
    # Pull LDAP Data
    import_data_list = ldap_pull.ldap_pull_data(ldap_handler, ldap_mappings, logger)
    import_data_dicts = [asdict(x) for x in import_data_list]
    logger.debug(f"import data request:\n{json.dumps(import_data_dicts, indent=4)}")

    # Sync to Cloudshell
    try:
        sync_cloudshell_groups(api, import_data_list, logger)
    except Exception as e:
        err_msg = f"Issue syncing groups to cloudshell. {type(e).__name__}: {str(e)}"
        logger.error(err_msg)
        raise exceptions.CloudshellSyncGroupsException(err_msg)
