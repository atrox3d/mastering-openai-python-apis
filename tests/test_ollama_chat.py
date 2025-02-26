import pytest

from helpers.ollama import chat
from helpers.ollama import ollamamanager as om
from helpers.ollama import defaults

HOST = '192.168.1.10'


def test_chat():
    messages = [chat.user_message('are you llama3.2 llm model? so its free of cost?')]
    reply = (chat.ask(
        *messages,
        client=chat.get_client(HOST, defaults.PORT),
        model='llama3.2'
    ))
    print(chat.get_message_content(reply))
