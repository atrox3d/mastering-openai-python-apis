document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const prompt = form.elements.prompt.value
        form.elements.prompt.value = ''

        fetch('/palette', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                prompt: prompt
            })
        })
        .then((response) => response.json())
        .then(data => {
            const colors = data.colors;
            const container = document.querySelector('.container');
            container.innerHTML = '';
            createColorBoxes(colors, container);

        });
    });
});

function createColorBoxes(colors, parent) {
    for(const color of colors) {
        const div = document.createElement('div')
        div.classList.add('color')
        div.style.backgroundColor = color;
        div.style.width = `calc(100%/ ${colors.length}`;
        div.addEventListener('click', function(){
            navigator.clipboard.writeText(color);
        });
        const span = document.createElement('span');
        span.innerText = color;
        div.appendChild(span);
        parent.appendChild(div);
    }
}
