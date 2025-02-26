import os
from pathlib import Path

import openai
from dotenv import load_dotenv



def check_openai_key() -> bool:
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is None:
        print('missing env variable OPENAI_API_KEY')
        if not Path('.env').exists():
            print('and no .env file found')
        print('exiting')
        return False
    print(f'openai apikey found: {api_key[:20]}...')
    return True


if __name__ == "__main__":
    if not check_openai_key():
        exit(1)
