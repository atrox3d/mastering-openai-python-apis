from dotenv import load_dotenv
import os
import openai

from pathlib import Path

from openai.types.chat.chat_completion import ChatCompletion
from helpers import defaults

CLIENT = None


def check_openai_key(
        dotenv_path     :str = defaults.DOTENV,
        apikey_env_var  :str = defaults.APIKEY_ENV_VAR
) -> bool:
    '''loads .env if present and check for apikey env var'''
    load_dotenv(dotenv_path)
    api_key = os.getenv(apikey_env_var)
    if api_key is None:
        print(f'missing env variable {apikey_env_var}')
        if not Path(dotenv_path).exists():
            print('and no .env file found')
        print('exiting')
        return False
    print(f'openai apikey found: {api_key[:20]}...')
    return True


def get_client() -> openai.OpenAI:
    '''get openai client singleton style'''
    global CLIENT
    CLIENT = CLIENT or openai.OpenAI()
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


def ask(
        *messages   :str,
        client      :openai.OpenAI = get_client(),
        model       :str           = defaults.MODEL,
        **kwargs
) -> ChatCompletion:
    '''query openai llm and returns full reply'''
    reply = client.chat.completions.create(
        messages=messages,
        model=model,
        **kwargs
    )
    return reply
