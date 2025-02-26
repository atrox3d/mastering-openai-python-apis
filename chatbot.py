import json
import os
from pathlib import Path

import openai
from openai.types.chat.chat_completion import ChatCompletion
from dotenv import load_dotenv


MODEL = 'gpt-4o-mini'
DOTENV = '.env'
APIKEY_ENV_VAR = 'OPENAI_API_KEY'
CLIENT = None
STOP_COMMANDS = 'bye stop end quit abort'.split()


def check_openai_key(dotenv:str=DOTENV, apikey_env_var:str=APIKEY_ENV_VAR) -> bool:
    '''loads .env if present and check for apikey env var'''
    load_dotenv()
    api_key = os.getenv(APIKEY_ENV_VAR)
    if api_key is None:
        print(f'missing env variable {APIKEY_ENV_VAR}')
        if not Path(dotenv).exists():
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


def ask(prompt:str, client:openai.OpenAI=get_client(), model=MODEL, **kwargs) -> ChatCompletion:
    '''query openai llm and returns full reply'''
    reply = client.chat.completions.create(
        messages=[user_message(prompt)],
        model=model,
        **kwargs
    )
    return reply


def user_input(prompt:str='You: ') -> str:
    '''get prompt from user'''
    return input(prompt)


def proceed(prompt:str, stop_commands:list[str]=STOP_COMMANDS) -> bool:
    '''check if user wants to stop'''
    return prompt.lower() not in stop_commands


def process_answer(reply:ChatCompletion):
    '''do whatever is needed with the answer'''
    answer = reply.choices[0].message.content
    print(f'Bot: {answer}')


def main():
    '''main entry, will be wrapped in typer'''
    if not check_openai_key():
        exit(1)
    try:
        while True:
            prompt = user_input()
            if proceed(prompt):
                reply = ask(prompt)
                process_answer(reply)
            else:
                break
    except KeyboardInterrupt:
        pass
    finally:
        print('exiting...')



if __name__ == "__main__":
    main()