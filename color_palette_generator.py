import json
from pathlib import Path
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request
from ipynb.fs.defs.color_palette_generator import (
    get_llm_response,
    get_color_palette,
    get_colors_prompt
)

load_dotenv()

client = openai.OpenAI()

TEMPLATES = 'templates'
STATIC_FILES = 'static'
Path(TEMPLATES).mkdir(exist_ok=True)
Path(STATIC_FILES).mkdir(exist_ok=True)
app = Flask(
        __name__, 
        static_folder=STATIC_FILES,
        static_url_path='',
        template_folder=TEMPLATES
    )

WORDLIST = ['example']


def get_funny_word(client:openai.OpenAI) -> str:
    app.logger.info('generating funny word')
    rag_words = ', '.join(WORDLIST)
    
    prompt = f'''
        give me a random funny word not present in this list: "{rag_words}"
        - use timestamp to randomize word generation
        - desired output: only the funnyword, nothing else
        '''
    app.logger.info(prompt)
    funnyword = get_llm_response(
        client, 
        prompt
    )
    WORDLIST.append(funnyword)
    
    app.logger.info(f'{funnyword = }')
    app.logger.info(f'{WORDLIST = }')
    return funnyword


@app.post('/palette')
def palette():
    try:
        prompt = request.form.get('prompt')
        app.logger.info(f'{prompt = }')
        colors = get_color_palette(client, prompt)
        response =  {'colors': colors}
        app.logger.info(f'{response = }')
        return response
    except json.JSONDecodeError as jde:
        app.logger.error(f'{prompt = }')
        return {'colors':[]}

@app.get('/')
def index():
    # return render_template('index.html')
    return render_template('index.html')

    funnyword = get_funny_word(client)
    return f'ChatGPT says: {funnyword}'

if __name__ == "__main__":
    app.run(
        debug=True
    )
