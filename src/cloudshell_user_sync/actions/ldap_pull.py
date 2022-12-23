"""
Module to combine the ldap api actions and cloudshell sync flow
"""
import logging
from typing import List

from cloudshell_user_sync.models.config import LdapGroupsMapping
from cloudshell_user_sync.models.cs_import import ImportGroupData
from cloudshell_user_sync.utility.ldap3_handler import Ldap3Handler
from cloudshell_user_sync import exceptions


def ldap_pull_data(ldap_handler: Ldap3Handler,
                   ldap_mappings: List[LdapGroupsMapping],
                   logger: logging.Logger) -> List[ImportGroupData]:
    import_data_list = []
    for curr_mapping in ldap_mappings:
        try:
            ldap_users = ldap_handler.get_user_data_for_group_cn(curr_mapping.ldap_cn)
        except Exception as e:
            err_msg = f"Issue getting ldap data for group cn {curr_mapping.ldap_cn}: {str(e)}"
            logger.error(err_msg)
            raise exceptions.LdapHandlerException(err_msg)
        user_names = [x.sam_account_name for x in ldap_users]
        import_data = ImportGroupData(ldap_group_cn=curr_mapping.ldap_cn,
                                      users=user_names,
                                      target_cloudshell_groups=curr_mapping.cloudshell_groups)
        import_data_list.append(import_data)
    return import_data_list
