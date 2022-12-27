import pytest
from cloudshell.api.cloudshell_api import CloudShellAPISession
from logger_stdout import get_logger


@pytest.fixture(scope="session")
def std_out_logger() -> CloudShellAPISession:
    return get_logger("test logger")
