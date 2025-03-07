# load_dotenv()
# client = openai.OpenAI()
# embed_client = ollama.Client()


import time


def retry(wait:int=2, max_retries:int=5):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    result = func(*args, **kwargs)
                    return result
                except:
                    print(f'function call failed, attempts: {attempts}/{max_retries}')
                    if attempts >= max_retries:
                        print('giving up')
                        break
                    attempts +=1
                    print(f'waiting {wait} seconds...')
                    time.sleep(wait)
        return wrapper
    return decorator