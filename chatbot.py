import json

from openai.types.chat.chat_completion import ChatCompletion
import typer

from helpers import defaults
from helpers.openai import (
        check_openai_key,
        message,
        user_message,
        assistant_message,
        ask,
        get_message_content,
        setup_history,
)


def user_input(prompt:str='You: ') -> str:
    '''get prompt from user'''
    return input(prompt)


def proceed(
        prompt          :str, 
        stop_commands   :list[str] = defaults.STOP_COMMANDS
) -> bool:
    '''check if user wants to stop'''
    return prompt.lower() not in stop_commands


def process_answer(reply:ChatCompletion):
    '''do whatever is needed with the answer'''
    answer = get_message_content(reply)
    print(f'Bot: {answer}')


#
#   TODO: find a way to run commands with params or globals
#
COMMANDS = {
    '/history': {'fn': None, 'args':['history']}
}
def command(prompt:str, commands:dict=COMMANDS, **kwargs):
    # if prompt.startswith('/') and any(prompt.startswith(cmd) for cmd in commands.keys()):
    for cmd in commands.keys():
        if prompt.startswith(cmd):
            # TODO: process command
            cmd, *rest = cmd.split()
            print(f'command!', cmd, rest)
            return True
    return False
#
#   TODO: find a way to run commands with params or globals
#


def main(
        model       :str = defaults.MODEL, 
        dotenv_path :str = defaults.DOTENV,
        apikey_env  :str = defaults.APIKEY_ENV_VAR,
        user_prompt :str = 'You: ',
        personality :str = None,
        system      :str = None,
        developer   :str = None,
):
    '''main entry, will be wrapped in typer'''
    if not check_openai_key(dotenv_path, apikey_env):
        exit(1)
    try:
        history = []
        setup_history(history, system, developer, personality)
        
        while True:
            prompt = user_input(user_prompt)
            if command(prompt):
                continue
            
            if proceed(prompt):
                history.append(user_message(prompt))
                reply = ask(*history, model=model)
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
