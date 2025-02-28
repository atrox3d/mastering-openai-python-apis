# from dotenv import load_dotenv
import os
import ollama
from pathlib import Path

from helpers.ollama import defaults
from helpers.ollama import ollamamanager

CLIENT = None

def get_client(host, port) -> ollama.Client:
    '''get openai client singleton style'''
    global CLIENT
    CLIENT = CLIENT or ollama.Client(
        ollamamanager.get_server(host, port)
    )
    return CLIENT


def message(role:str, content:str) -> dict:
    '''creates message dict'''
    return {'role': role, 'content': content}


def user_message(content:str) -> dict:
    return message('user', content)


def system_message(content:str) -> dict:
    return message('system', content)


def dev_message(content:str) -> dict:
    return message('developer', content)


def assistant_message(content:str) -> dict:
    return message('assistant', content)


def get_message_content(completion:ollama.ChatResponse) -> str:
    return completion.message.content


def setup_history(
        history     :list,
        system      :str = None,
        developer   :str = None,
        personality :str = None
) -> list:
    if system is not None:
        print(f'adding system message: {system}')
        history.append(system_message(system))
    if developer is not None:
        print(f'adding developer message: {developer}')
        history.append(dev_message(developer))
    if personality is not None:
        history.append(system_message(f'your personality is {personality}'))
        print(f'adding personality: {personality}')
    return history


def ask(
        *messages   :str,
        client      :ollama.Client,
        model       :str           = defaults.MODEL,
        **kwargs
) -> ollama.ChatResponse:
    '''query openai llm and returns full reply'''
    reply = client.chat(
        messages=messages,
        model=model,
        **kwargs
    )
    return reply
