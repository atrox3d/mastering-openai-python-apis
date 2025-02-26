from helpers.ollama import ollamamanager as om


def test_ssh():
    om.start_remote_ollama('192.168.1.10')