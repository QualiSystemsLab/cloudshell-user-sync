from typing import List, Dict
from dataclasses import dataclass
from ldap3 import Server, Connection, ALL


@dataclass
class LdapUserData:
    uid: str
    cn: str
    email: str


class Ldap3Handler:
    def __init__(self, server: str, user_dn: str, password: str, search_base_dn: str):
        self._server = server
        self._user_dn = user_dn
        self._password = password
        self._search_base_dn = search_base_dn
        self._conn = self._get_connection()

    def _get_connection(self):
        ldap_server = Server(self._server, get_info=ALL)
        return Connection(server=ldap_server, user=self._user_dn, password=self._password, auto_bind=True)

    @staticmethod
    def _get_uid_substring_from_dn(self, user_dn):
        segments = user_dn.split(",")
        uid_segment_filter = [segment for segment in segments if "uid" in segment]
        if uid_segment_filter:
            return uid_segment_filter[0]
        else:
            raise Exception("'uid' not found in user dn string: {}".format(user_dn))

    def get_all_groups_dn_list(self) -> List[str]:
        with self._conn:
            is_found = self._conn.search(
                search_base=self._search_base_dn,
                search_filter='(objectClass=organizationalUnit)',
                search_scope='SUBTREE',
                attributes=["*"]
            )
            if not is_found:
                raise ValueError(f"No group entries found for search base '{self._search_base_dn}'")
        return [x.entry_dn for x in self._conn.entries]

    def get_group_users(self, group_dn: str) -> List[LdapUserData]:
        with self._conn:
            self._conn.search(search_base=group_dn,
                              search_filter='(objectClass=organizationalPerson)',
                              attributes=["*"])
            return [LdapUserData(x.uid.value, x.cn.value, x.mail.value) for x in self._conn.entries]

    def get_groups_table(self, group_dn_list: List[str]) -> Dict[str, List[LdapUserData]]:
        result = {}
        for group_dn in group_dn_list:
            users = self.get_group_users(group_dn)
            result[group_dn] = users
        return result

    def get_all_groups_table(self) -> Dict[str, List[LdapUserData]]:
        group_dn_list = self.get_all_groups_dn_list()
        return self.get_groups_table(group_dn_list)


if __name__ == "__main__":
    LDAP_SERVER_URI = 'ldap://localhost'
    LDAP_USER_DN = 'cn=Manager,dc=my-domain,dc=com'
    LDAP_PASSWORD = 'secret'
    LDAP_SEARCH_BASE = 'dc=my-domain,dc=com'

    handler = Ldap3Handler(LDAP_SERVER_URI, LDAP_USER_DN, LDAP_PASSWORD, LDAP_SEARCH_BASE)
    users_table = handler.get_groups_table()
    pass