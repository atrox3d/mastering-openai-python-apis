import pytest
from helpers.ollama import ollamamanager as om
from helpers.ollama import defaults


HOST = '192.168.1.10'

def test_is_server_ready_or_abort_tests():
    ready = om.is_server_ready(HOST, defaults.PORT)
    if not ready:
        pytest.exit('server is not ready')


def test_wait_for_server_or_abort_tests():
    try:
        om.wait_for_server(
            HOST,
            defaults.PORT,
            defaults.WAIT_SECONDS,
            defaults.ATTEMPTS
        )
    except TimeoutError:
        pytest.exit('server is not ready')


def test_is_ollama_up():
    try:
        assert om.is_ollama_up(HOST)
    except AssertionError:
        pytest.exit('server is not ready')


def test_is_local():
    assert om.is_local('localhost')
    assert om.is_local('127.0.0.1')
    assert not om.is_local(HOST)


def test_cannot_start_remote_ollama():
    with pytest.raises(om.RemoteOllamaServiceException):
        om.start_ollama(HOST)


def test_cannot_stop_remote_ollama():
    with pytest.raises(om.RemoteOllamaServiceException):
        om.start_ollama(HOST)


def test_remote_ollama_ctx_raises_exception():
    with pytest.raises(om.RemoteOllamaServiceException):
        with om.OllamaServerCtx(HOST, stop=False):
            pass
