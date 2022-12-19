from cloudshell_user_sync.utility import keyring_handler


def test_no_creds():
    cs_creds = keyring_handler.get_cs_creds()
    pass
