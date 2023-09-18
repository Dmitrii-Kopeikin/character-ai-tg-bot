const tg = window.Telegram.WebApp;

const cards = document.getElementsByClassName('character-card');
let selected = false;

function clickCard(event) {
    if (selected === true) {
        return;
    }
    selected = true;
    const card = event.target.closest('.character-card');
    const id = card.getAttribute('data-id');
    const urlParams = new URLSearchParams(window.location.search);
    const user_tg_id = urlParams.get('user_tg_id');

    result = fetch(`/choose_character`, {
        method: 'POST',
        body: JSON.stringify({
            character_id: id,
            user_tg_id: user_tg_id,
        }),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
        },
    }).then(() => {
        tg.close();
    });
}

for (const card of cards) {
    card.addEventListener('click', clickCard, { once: true });
}
