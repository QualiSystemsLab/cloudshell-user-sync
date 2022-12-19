import ldap3
from ldap3 import Entry


BASE_DN = "DC=natticorp,DC=example,DC=com"
TARGET_GROUP = "nattigroup"
TARGET_GROUP_DN = f'CN={TARGET_GROUP},{BASE_DN}'
SERVER_IP = "192.168.85.114"
LOGIN_USER = "Administrator"
LOGIN_PASSWORD = "Password1"

# Connect to the LDAP server
server = ldap3.Server(host=f'ldap://{SERVER_IP}')
conn = ldap3.Connection(server=server,
                        user=f"CN={LOGIN_USER},CN=Users,{BASE_DN}",
                        password=LOGIN_PASSWORD)

search_filter = f'(&(objectClass=user)(memberOf={TARGET_GROUP_DN}))'

with conn:
    # conn.bind()
    is_found = conn.search(
        search_base=BASE_DN,
        search_filter=search_filter,
        # search_scope='SUBTREE',
        attributes=["*"]
    )
    user_entries = conn.entries

for user_entry in user_entries:
    print(f"CN: {user_entry['cn']}")
    attrs_list = user_entry.entry_attributes
    if "mail" in attrs_list:
        print(f"mail: {user_entry['mail']}")
    else:
        print("no mail found")


with conn:
    # conn.bind()
    is_found = conn.search(
        search_base=BASE_DN,
        search_filter='(cn=nattigroup)',
        # search_scope='SUBTREE',
        attributes=["*"]
    )
    entries = conn.entries
    if not entries:
        raise ValueError("group not found")
    members = entries[0].member.values
    pass
conn.search('dc=example,dc=com', search_filter, attributes=['cn', 'mail'])

