/**
 * AI Көмекші - демо чат
 * Университеттің қызметі бойынша AI агент
 */

(function() {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    const responses = {
        'сәлем': 'Сәлеметсіз бе! Қандай көмек керек?',
        'салем': 'Сәлеметсіз бе! Қандай көмек керек?',
        'келесі': 'Келесі сынып кестесін білу үшін деканатпен хабарласыңыз немесе студент порталын қараңыз.',
        'кесте': 'Кесте туралы ақпарат студент порталында немесе деканатта бар. Қосымша сұрағыңыз бар ма?',
        'құжат': 'Құжат сұрау үшін жеке кабинетке кіріп "Құжат сұрау" бөліміне өтіңіз.',
        'справка': 'Справка алу үшін деканатқа өтініш беріңіз. Жеке кабинет арқылы да сұрау жасауға болады.',
        'емтихан': 'Емтихан кестесі әдетте семестр соңында жарияланады. Нақты күндер туралы деканаттан хабарласыңыз.',
        'деканат': 'Деканатпен байланыс: пошта арқылы немесе жеке келу. Жұмыс уақыты: дүйсенбі-жұма 9:00-18:00.',
        'рахмет': 'Оқасы жоқ! Басқа сұрағыңыз болса, сұраңыз.',
        'көмек': 'Мен университет қызметі бойынша көмектесемін: кесте, құжаттар, процедуралар туралы сұрақтарға жауап бере аламын.',
        'default': 'Түсінікті. Бұл сұрақ бойынша деканатпен немесе оқытушымен хабарласыңыз. Басқа сұрағыңыз бар ма?'
    };

    function getResponse(text) {
        const lower = text.toLowerCase().trim();
        for (const [key, value] of Object.entries(responses)) {
            if (lower.includes(key) && key !== 'default') return value;
        }
        return responses.default;
    }

    function addMessage(content, isUser) {
        const div = document.createElement('div');
        div.className = 'chat-message ' + (isUser ? 'user-message' : 'bot-message');
        div.innerHTML = isUser
            ? `<div class="message-avatar"><i class="bi bi-person-fill"></i></div>
               <div class="message-content"><strong>Сіз:</strong><p class="mb-0">${content}</p></div>`
            : `<div class="message-avatar"><i class="bi bi-robot"></i></div>
               <div class="message-content"><strong>AI Көмекші:</strong><p class="mb-0">${content}</p></div>`;
        chatContainer.appendChild(div);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;
        addMessage(text, true);
        userInput.value = '';
        setTimeout(function() {
            addMessage(getResponse(text), false);
        }, 500);
    }

    if (sendBtn) sendBtn.addEventListener('click', sendMessage);
    if (userInput) userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
})();
