from ipynb.fs.defs.color_palette_generator import (
    openai,
    load_dotenv,
    get_llm_response
)

load_dotenv()

client = openai.OpenAI()

print(get_llm_response(client, 'testing'))

