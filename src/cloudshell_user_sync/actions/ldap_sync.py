"""
Module to combine the ldap api actions and cloudshell sync flow
"""
import json
import logging
from typing import List

from cloudshell_user_sync.actions.cloudshell_sync import SyncGroupsAction
from cloudshell_user_sync.models import config, cs_import
from cloudshell_user_sync.utility.ldap3_handler import Ldap3Handler
from cloudshell_user_sync import exceptions
from cloudshell.api.cloudshell_api import CloudShellAPISession
from dataclasses import asdict


def run_ldap_sync(api: CloudShellAPISession,
                  ldap_handler: Ldap3Handler,
                  ldap_mappings: List[config.LdapGroupsMapping],
                  logger: logging.Logger):
    # get user data from LDAP
    import_data_list = []
    for curr_mapping in ldap_mappings:
        try:
            ldap_users = ldap_handler.get_user_data_for_group_cn(curr_mapping.ldap_cn)
        except Exception as e:
            err_msg = f"Issue getting ldap data for group cn {curr_mapping.ldap_cn}: {str(e)}"
            logger.error(err_msg)
            raise exceptions.LdapHandlerException(err_msg)
        user_names = [x.cn for x in ldap_users]
        import_data = cs_import.ImportGroupData(ldap_group_cn=curr_mapping.ldap_cn,
                                                users=user_names,
                                                target_cloudshell_groups=curr_mapping.cloudshell_groups)
        import_data_list.append(import_data)

    # debug print the sync request data
    import_data_dicts = [asdict(x) for x in import_data_list]
    logger.debug(f"import data request:\n{json.dumps(import_data_dicts, indent=4)}")

    # sync the request into Cloudshell
    try:
        sync_action = SyncGroupsAction(api, import_data_list, logger)
        sync_action.sync_groups()
    except Exception as e:
        err_msg = f"Issue syncing groups to cloudshell. {type(e).__name__}: {str(e)}"
        logger.error(err_msg)
        raise exceptions.CloudshellSyncGroupsException(err_msg)
