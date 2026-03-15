/**
 * AI Көмекші - чат (Django API немесе локальды жауаптар)
 */
(function() {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    if (!chatContainer || !userInput) return;

    const chatApiUrl = chatContainer.getAttribute('data-chat-url');
    let chatHistory = [];
    let isLoading = false;

    const localResponses = {
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
        'баға': 'Бағаларыңызды көру үшін жеке кабинеттегі "Бағалар" бөліміне өтіңіз.',
        'default': 'Түсінікті. Бұл сұрақ бойынша деканатпен немесе оқытушымен хабарласыңыз. Басқа сұрағыңыз бар ма?'
    };

    function getLocalResponse(text) {
        const lower = text.toLowerCase().trim();
        for (const [key, value] of Object.entries(localResponses)) {
            if (key !== 'default' && lower.includes(key)) return value;
        }
        return localResponses.default;
    }

    function addMessage(content, isUser, elementId) {
        const div = document.createElement('div');
        div.className = 'chat-message ' + (isUser ? 'user-message' : 'bot-message');
        if (elementId) div.id = elementId;
        div.innerHTML = isUser
            ? '<div class="message-avatar"><i class="bi bi-person-fill"></i></div><div class="message-content"><strong>Сіз:</strong><p class="mb-0">' + escapeHtml(content) + '</p></div>'
            : '<div class="message-avatar"><i class="bi bi-robot"></i></div><div class="message-content"><strong>AI Көмекші:</strong><p class="mb-0">' + escapeHtml(content) + '</p></div>';
        chatContainer.appendChild(div);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return div;
    }

    function addLoadingIndicator() {
        const div = document.createElement('div');
        div.id = 'chat-loading';
        div.className = 'chat-message bot-message';
        div.innerHTML = '<div class="message-avatar"><i class="bi bi-robot"></i></div><div class="message-content"><strong>AI Көмекші:</strong><p class="mb-0"><span class="chat-loading-dots"><span>.</span><span>.</span><span>.</span></span></p></div>';
        chatContainer.appendChild(div);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return div;
    }

    function removeLoadingIndicator() {
        const el = document.getElementById('chat-loading');
        if (el) el.remove();
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function setLoading(loading) {
        isLoading = loading;
        if (sendBtn) {
            sendBtn.disabled = loading;
            sendBtn.innerHTML = loading ? '<span class="spinner-border spinner-border-sm me-1"></span>Жіберілуде...' : '<i class="bi bi-send-fill"></i> Жіберу';
        }
        userInput.disabled = loading;
    }

    function sendMessage() {
        const text = userInput.value.trim();
        if (!text || isLoading) return;

        addMessage(text, true);
        chatHistory.push({ role: 'user', content: text });
        userInput.value = '';
        setLoading(true);

        if (chatApiUrl) {
            addLoadingIndicator();
            fetch(chatApiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ message: text, history: chatHistory.slice(0, -1).slice(-10) }),
                credentials: 'same-origin'
            })
            .then(r => r.json())
            .then(function(data) {
                removeLoadingIndicator();
                const resp = data.response || data.error || 'Қате';
                addMessage(resp, false);
                chatHistory.push({ role: 'assistant', content: resp });
            })
            .catch(function() {
                removeLoadingIndicator();
                const resp = getLocalResponse(text);
                addMessage(resp, false);
                chatHistory.push({ role: 'assistant', content: resp });
            })
            .finally(function() { setLoading(false); });
        } else {
            setTimeout(function() {
                const resp = getLocalResponse(text);
                addMessage(resp, false);
                chatHistory.push({ role: 'assistant', content: resp });
                setLoading(false);
            }, 500);
        }
    }

    if (sendBtn) sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
})();
