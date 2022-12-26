from cloudshell_user_sync.utility import keyring_handler


def test_cs_creds_set_get():
    user, password = "admin", "admin"
    keyring_handler.set_cloudshell_keyring(user, password)
    cs_creds = keyring_handler.get_cs_creds()
    assert cs_creds.username == user
    assert cs_creds.password == password
