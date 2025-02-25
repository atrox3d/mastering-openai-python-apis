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
Path(TEMPLATES).mkdir(exist_ok=True)
app = Flask(__name__, template_folder=TEMPLATES)

WORDLIST = ['example']


@app.post('/palette')
def palette():
    prompt = request.form.get('prompt')
    return {'colors': get_color_palette(client, prompt)}



@app.get('/')
def index():
    # return render_template('index.html')
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
    return f'ChatGPT says: {funnyword}'

if __name__ == "__main__":
    app.run(
        debug=True
    )
