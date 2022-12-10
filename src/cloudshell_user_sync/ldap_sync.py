"""
Module to combine the ldap api actions and cloudshell sync flow
"""
import logging

from cloudshell_user_sync.cloudshell_sync import SyncInboundGroupsAction
from cloudshell_user_sync import config_handler
from cloudshell_user_sync.models import cs_import
from cloudshell_user_sync import ldap3_handler
from cloudshell_user_sync import exceptions


def run_ldap_sync(json_config_path: str, logger: logging.Logger):
    ldap_config = config_handler.get_ldap_config_from_json(json_config_path)
    api = config_handler.get_api_from_cs_config(ldap_config.cloudshell_details, logger)
    ldap_details = ldap_config.ldap_details
    ldap = ldap3_handler.Ldap3Handler(server=ldap_details.server,
                                      user_dn=ldap_details.user_dn,
                                      password=ldap_details.password,
                                      search_base_dn=ldap_details.search_base)
    group_dn_list = [x.ldap_dn for x in ldap_config.ldap_mappings]
    group_dn_map = {x.ldap_dn: x.cloudshell_groups for x in ldap_config.ldap_mappings}
    try:
        dn_groups_dict = ldap.get_groups_table(group_dn_list)
    except Exception as e:
        err_msg = f"Failed LDAP call. {type(e).__name__}: {str(e)}"
        logger.error(err_msg)
        raise exceptions.LdapHandlerException(err_msg)

    inbound_groups_data = []
    for dn_group_id in dn_groups_dict:
        inbound_data = cs_import.InboundGroupData(external_group_uid=dn_group_id,
                                                  target_cloudshell_groups=group_dn_map[dn_group_id],
                                                  inbound_users=dn_groups_dict[dn_group_id])
        inbound_groups_data.append(inbound_data)

    try:
        sync_action = SyncInboundGroupsAction(api, inbound_groups_data, logger)
        sync_action.sync_inbound_groups()
    except Exception as e:
        err_msg = f"Issue syncing groups to cloudshell. {type(e).__name__}: {str(e)}"
        logger.error(err_msg)
        raise exceptions.CloudshellSyncGroupsException(err_msg)
