from typing import List

import ldap3
from ldap3 import Entry


def get_all_groups_entries(conn, base_dn) -> List[Entry]:
    with conn:
        is_found = conn.search(search_base=base_dn, search_filter="(objectClass=group)", attributes=["*"])
        if not is_found:
            raise ValueError(f"No group entries found in base DN '{base_dn}'")
        group_entries = conn.entries
    return group_entries


if __name__ == "__main__":
    BASE_DN = "DC=natticorp,DC=example,DC=com"
    TARGET_GROUP = "nattigroup"
    TARGET_GROUP_DN = f"CN={TARGET_GROUP},{BASE_DN}"
    SERVER_IP = "192.168.85.114"
    LOGIN_USER = "CN=Administrator,CN=Users,DC=natticorp,DC=example,DC=com"
    LOGIN_PASSWORD = "Password1"

    # Connect to the LDAP server
    server = ldap3.Server(host=f"ldap://{SERVER_IP}")
    conn = ldap3.Connection(server=server, user=LOGIN_USER, password=LOGIN_PASSWORD)
    group_entries = get_all_groups_entries(conn, BASE_DN)
    print(f"found {len(group_entries)} entries")
