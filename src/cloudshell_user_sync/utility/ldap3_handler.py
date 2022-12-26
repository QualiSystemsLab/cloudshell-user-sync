from dataclasses import dataclass
from typing import List

from ldap3 import ALL, Connection, Entry, Server

SAM_ACCOUNT_NAME_ATTR = "sAMAccountName"


@dataclass
class LdapUserData:
    cn: str
    sam_account_name: str
    email: str


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
            is_found = self.conn.search(search_base=self.base_dn, search_filter="(objectClass=group)", attributes=["*"])
            if not is_found:
                raise ValueError(f"No group entries found in base DN '{self.base_dn}'")
            group_entries = self.conn.entries
        return group_entries

    def get_custom_group_entries(self) -> List[Entry]:
        all_entries = self.get_all_groups_entries()
        return self._filter_for_custom_groups(all_entries)

    def get_custom_group_distinguished_names(self):
        custom_entries = self.get_custom_group_entries()
        return [x.cn.value for x in custom_entries]

    def _get_user_entries_for_group_cn(self, group_cn: str) -> List[Entry]:
        group_dn = f"CN={group_cn},{self.base_dn}"
        search_filter = f"(&(objectClass=user)(memberOf={group_dn}))"
        with self.conn:
            is_found = self.conn.search(search_base=self.base_dn, search_filter=search_filter, attributes=["*"])
            if not is_found:
                raise ValueError(f"No entries found for group {group_dn}")
            user_entries = self.conn.entries
        return user_entries

    def get_user_data_for_group_cn(self, group_cn: str):
        result = []
        user_entries = self._get_user_entries_for_group_cn(group_cn)
        for entry in user_entries:
            cn = entry["cn"].value
            attrs = entry.entry_attributes
            if SAM_ACCOUNT_NAME_ATTR in attrs:
                sam_account_name = entry[SAM_ACCOUNT_NAME_ATTR].value
            else:
                sam_account_name = ""
            if "mail" in attrs:
                email = entry["mail"].value
            else:
                email = ""
            user_data = LdapUserData(cn=cn, sam_account_name=sam_account_name, email=email)
            result.append(user_data)
        return result


if __name__ == "__main__":
    LDAP_SERVER = "192.168.85.114"
    LDAP_USER_DN = "CN=Administrator,CN=Users,DC=natticorp,DC=example,DC=com"
    LDAP_PASSWORD = "Password1"
    LDAP_BASE_DN = "DC=natticorp,DC=example,DC=com"

    handler = Ldap3Handler(LDAP_SERVER, LDAP_USER_DN, LDAP_PASSWORD, LDAP_BASE_DN)
    custom_groups = handler.get_custom_group_distinguished_names()
    print(f"custom groups found: {len(custom_groups)}")
