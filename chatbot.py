import json
import os
from pathlib import Path

import openai
from openai.types.chat.chat_completion import ChatCompletion
from dotenv import load_dotenv
import typer


MODEL = 'gpt-4o-mini'
DOTENV = '.env'
APIKEY_ENV_VAR = 'OPENAI_API_KEY'
CLIENT = None
STOP_COMMANDS = 'bye stop end quit abort exit'.split()


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


def user_input(prompt:str='You: ') -> str:
    '''get prompt from user'''
    return input(prompt)


def proceed(prompt:str, stop_commands:list[str]=STOP_COMMANDS) -> bool:
    '''check if user wants to stop'''
    return prompt.lower() not in stop_commands


def get_message_content(completion:ChatCompletion) -> str:
    content = completion.choices[0].message.content
    return content


def process_answer(reply:ChatCompletion):
    '''do whatever is needed with the answer'''
    answer = get_message_content(reply)
    print(f'Bot: {answer}')


def ask(*messages:str, client:openai.OpenAI=get_client(), model=MODEL, **kwargs) -> ChatCompletion:
    '''query openai llm and returns full reply'''
    reply = client.chat.completions.create(
        messages=messages,
        model=model,
        **kwargs
    )
    return reply


def main():
    '''main entry, will be wrapped in typer'''
    if not check_openai_key():
        exit(1)
    try:
        history = []
        while True:
            prompt = user_input()
            if proceed(prompt):
                
                history.append(user_message(prompt))
                reply = ask(*history)
                history.append(assistant_message(get_message_content(reply)))
                
                process_answer(reply)
            else:
                break
    except KeyboardInterrupt:
        pass
    finally:
        print('exiting...')



if __name__ == "__main__":
    app = typer.Typer(add_completion=False)
    app.command('main')(main)
    app()