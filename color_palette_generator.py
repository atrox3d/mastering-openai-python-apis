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

app = Flask(
    __name__,
    template_folder=TEMPLATES
)

@app.post('/palette')
def palette():
    ...


wordlist = ['example']

@app.get('/')
def index():
    # return render_template('index.html')
    app.logger.info('generating funny word')
    rag_words = ', '.join(wordlist)
    
    prompt = f'''
        give me a random funny word not present in this list: "{rag_words}"
        desired output: funnyword
        '''
    app.logger.info(prompt)
    funnyword = get_llm_response(
        client, 
        prompt
    )
    wordlist.append(funnyword)
    
    app.logger.info(f'{funnyword = }')
    return f'ChatGPT says: {funnyword}'

if __name__ == "__main__":
    app.run(
        debug=True
    )
