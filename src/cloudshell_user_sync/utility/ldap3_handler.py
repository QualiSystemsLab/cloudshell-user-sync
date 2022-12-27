"""
Cloudshell uses the LDAP/AD Sam Account Name attribute as the cloudshell user for imported users
"""
from dataclasses import dataclass
from typing import List

from ldap3 import ALL, Connection, Entry, Server

SAM_ACCOUNT_NAME_ATTR = "sAMAccountName"
DISTINGUISHED_NAME_ATTR = "distinguishedName"


@dataclass
class LdapUserData:
    sam_account_name: str
    email: str
    cn: str
    distinguished_name: str


class Ldap3Handler:
    def __init__(self, server: str, user_dn: str, password: str, base_dn: str):
        self.server = server
        self.base_dn = base_dn
        self.user_dn = user_dn
        self._password = password
        self.conn = self._get_connection()

    def _get_connection(self):
        ldap_server = Server(host=f"ldap://{self.server}", get_info=ALL)
        return Connection(server=ldap_server, user=self.user_dn, password=self._password)

    @staticmethod
    def _filter_for_custom_groups(group_entries: List[Entry]) -> List[Entry]:
        result = []
        for entry in group_entries:
            if "isCriticalSystemObject" in entry.entry_attributes:
                continue
            result.append(entry)
        return result

    def get_all_groups_entries(self) -> List[Entry]:
        with self.conn:
            self.conn.search(search_base=self.base_dn, search_filter="(objectClass=group)", attributes=["*"])
            group_entries = self.conn.entries
        return group_entries

    def get_custom_group_entries(self) -> List[Entry]:
        all_entries = self.get_all_groups_entries()
        return self._filter_for_custom_groups(all_entries)

    def get_custom_group_distinguished_names(self):
        custom_entries = self.get_custom_group_entries()
        return [x.cn.value for x in custom_entries]

    def get_user_entries_for_group_dn(self, group_dn: str) -> List[Entry]:
        search_filter = f"(&(objectClass=user)(memberOf={group_dn}))"
        with self.conn:
            self.conn.search(search_base=self.base_dn, search_filter=search_filter, attributes=["*"])
            user_entries = self.conn.entries
        return user_entries

    def get_user_data_for_group_dn(self, group_dn: str) -> List[LdapUserData]:
        result = []
        user_entries = self.get_user_entries_for_group_dn(group_dn)
        for entry in user_entries:
            cn = entry["cn"].value
            attrs = entry.entry_attributes
            sam_account_name = entry[SAM_ACCOUNT_NAME_ATTR].value if SAM_ACCOUNT_NAME_ATTR in attrs else ""
            email = entry["mail"].value if "mail" in attrs else ""
            user_dn = entry[DISTINGUISHED_NAME_ATTR].value if DISTINGUISHED_NAME_ATTR in attrs else ""
            user_data = LdapUserData(cn=cn, sam_account_name=sam_account_name, email=email, distinguished_name=user_dn)
            result.append(user_data)
        return result


if __name__ == "__main__":
    LDAP_SERVER = "<SERVER_IP>"
    LDAP_USER_DN = "CN=Administrator,CN=Users,DC=samplecorp,DC=example,DC=com"
    LDAP_PASSWORD = "<USER_PASSWORD>"
    LDAP_BASE_DN = "DC=natticorp,DC=example,DC=com"
    TARGET_GROUP_DN = "CN=mygroup,DC=samplecorp,DC=example,DC=com"

    handler = Ldap3Handler(LDAP_SERVER, LDAP_USER_DN, LDAP_PASSWORD, LDAP_BASE_DN)
    group_users = handler.get_user_data_for_group_dn(TARGET_GROUP_DN)
    print((f"Group: {TARGET_GROUP_DN}\n"
           f"Users Found: {len(group_users)}"))
