const tg = window.Telegram.WebApp;

const submitBtn = document.getElementById('submit-btn');

function submit(event) {
    event.preventDefault();

    form = event.target.closest('form');
    formData = new FormData(form);

    if (
        !formData.get('name') ||
        !formData.get('description') ||
        !formData.get('greetings') ||
        !formData.get('image') ||
        !formData.get('prompt')
    ) {
        alert('Заполните все поля!');
        return;
    }

    result = fetch('/create-character', {
        method: 'POST',
        body: formData,
    }).then(() => {
        tg.close();
    });
}

submitBtn.addEventListener('click', submit);
