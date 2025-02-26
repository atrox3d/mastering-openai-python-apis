import pytest
from helpers.ollama import ollamamanager as om
from helpers.ollama import defaults


def test_remote_ollama():
    ready = om.is_server_ready('192.168.1.10', defaults.PORT)
    if not ready:
        pytest.exit('server is not ready')


def test_other():
    print('hello')
