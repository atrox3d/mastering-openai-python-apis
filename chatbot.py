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


def check_openai_key(dotenv:str=DOTENV, apikey_env_var:str=APIKEY_ENV_VAR) -> bool:
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
    global CLIENT
    CLIENT = CLIENT or openai.OpenAI()
    return CLIENT


def message(role:str, content:str) -> dict:
    return {'role': role, 'content': content}


def ask(prompt:str, client:openai.OpenAI=get_client(), model=MODEL, **kwargs) -> ChatCompletion:
    reply = client.chat.completions.create(
        messages=[message('user', prompt)],
        model=model
    )
    return reply


def get_question(prompt:str='You: ') -> str:
    return input(prompt)


def proceed(prompt:str, STOP_COMMANDS:list[str]='bye stop end quit abort'.split()) -> bool:
    return prompt.lower() not in STOP_COMMANDS


def output(reply:ChatCompletion):
    answer = reply.choices[0].message.content
    print(f'Bot: {answer}')


def main():
    if not check_openai_key():
        exit(1)
    try:
        while True:
            prompt = get_question()
            if proceed(prompt):
                reply = ask(prompt)
                output(reply)
            else:
                break
    except KeyboardInterrupt:
        pass
    finally:
        print('exiting...')



if __name__ == "__main__":
    main()