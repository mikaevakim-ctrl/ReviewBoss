import streamlit as st
import requests
import json
import time

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(
    page_title="MagicTales | Personalized Therapy Stories",
    page_icon="🔮",
    layout="centered"
)

# Премиальный уютный стиль детской книги
st.markdown("""
<style>
    .stApp { background-color: #FAFAFC; }
    h1, h2, h3 { font-family: 'Cozy', 'Comic Sans MS', sans-serif !important; }
    div.stButton > button {
        background-color: #6366F1 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        font-size: 18px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# Волшебная анимация падающих звезд на фоне
st.components.v1.html("""
<div id="magic-canvas" style="position:fixed; top:0; left:0; width:100vw; height:100vh; pointer-events:none; z-index:-1; overflow:hidden; background: transparent;"></div>
<script>
const container = document.getElementById('magic-canvas');
const stars = ['✨', '🌙', '🌟', '🧸', '🦄'];
function createStar() {
    const star = document.createElement('div');
    star.innerText = stars[Math.floor(Math.random() * stars.length)];
    star.style.position = 'absolute'; star.style.top = '-50px'; star.style.left = Math.random() * 100 + 'vw';
    const size = Math.random() * 15 + 12; const duration = Math.random() * 10 + 7; const opacity = Math.random() * 0.25 + 0.05;
    star.style.fontSize = size + 'px'; star.style.transition = `transform ${duration}s linear, opacity ${duration}s linear`; star.style.opacity = opacity;
    container.appendChild(star);
    setTimeout(() => {
        star.style.transform = `translateY(110vh) translateX(${(Math.random() * 60 - 30)}px) rotate(${Math.random() * 360}deg)`;
        star.style.opacity = '0';
    }, 100);
    setTimeout(() => { star.remove(); }, duration * 1000 + 100);
}
setInterval(createStar, 800);
</script>
""", height=0, width=0)

# Бесплатная генерация сказки
def generate_magic_story(child_name, child_age, setting, challenge):
    api_key = st.secrets.get("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY")
    url = "https://openrouter.ai"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    system_instruction = (
        "You are a compassionate child psychologist and a master storyteller for kids. "
        "Your goal is to write a warm, beautifully structured therapeutic bedtime story based on the user's inputs. "
        "The story MUST be written in the same language as the child's name provided (If Russian name -> write in Russian, if English name -> write in English). "
        "Rules:\n"
        "1. Never use technical, AI, or corporate words. Sound 100% like a loving human writer.\n"
        "2. Make the child the main character who gracefully learns a lesson or overcomes a fear through a gentle metaphor.\n"
        "3. Keep it concise but magical (approx. 250-450 words), ideal for reading aloud before bed."
    )
    
    user_content = f"Write a cozy bedtime story for a child named {child_name}, age {child_age}. Setting: {setting}. Challenge: {challenge}."
    data = {
        "model": "google/gemini-2.5-flash:free",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_content}
        ]
    }
        
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=15)
        if response.status_code == 200:
            result = response.json()
            return result['choices']['message']['content'].strip()
        else:
            return "Ошибка магии. Пожалуйста, попробуйте еще раз! 🪄"
    except Exception:
        return "Сказочная пыль еще укладывается. Пожалуйста, попробуйте еще раз!"
# Инициализация состояния оплаты
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False

# --- 1. ЗАГОЛОВОК САЙТА ---
st.markdown("<h1 style='text-align: center; color: #4F46E5; margin-bottom: 0;'>🔮 MagicTales</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4B5563; font-size: 18px; margin-top: 5px;'>Именные терапевтические сказки для вашего малыша</p>", unsafe_allow_html=True)

st.write("")

# --- 2. ФОРМА ЗАКАЗА СКАЗКИ ---
with st.container(border=True):
    st.markdown("##### 📝 Заполните данные для создания сказки:")
    child_name = st.text_input("Как зовут вашего ребёнка?", placeholder="Например: Лео, София, Максим", max_chars=20)
    child_age = st.slider("Сколько лет вашему малышу?", min_value=2, max_value=10, value=5)
    setting = st.selectbox(
        "Где будет происходить действие сказки?",
        ["В затерянном волшебном лесу", "На далекой космической станции", "В секретном подводном королевстве", "В уютном замке на мягком облаке", "В долине добрых динозавров"]
    )
    challenge = st.selectbox(
        "Какую тему или каприз мы хотим мягко решить?",
        ["Боязнь темноты и ночных монстров", "Нежелание ложиться спать вовремя", "Неумение делиться своими игрушками", "Сложная адаптация и страх перед детским садиком", "Частые вспышки злости, обиды или капризы"]
    )
    
    st.write("---")
    # Маркетинговый блок с динамической ценой
    is_first_time = st.checkbox("✨ Это моя первая сказка на сайте (Получить скидку)", value=True)
    price = 190 if is_first_time else 290

st.write("")

# --- 3. ПЛАТЕЖНЫЙ ЭКРАН И ГЕНЕРАЦИЯ ---
if not st.session_state.payment_done:
    # Блок до оплаты
    st.markdown(f"<h4 style='text-align: center;'>Стоимость создания сказки: <b style='color:#6366F1;'>{price} ₽</b></h4>", unsafe_allow_html=True)
    st.write("Нажмите кнопку ниже, чтобы перейти к быстрой оплате. После оплаты ваша персональная сказка откроется автоматически!")
    
    # Ссылка на оплату (СБП, ЮMoney, перевод). Сюда ты вставишь свою бесплатную платежную ссылку.
    st.markdown("<a href='https://your-payment-link.com' target='_blank'><button style='width:100%; background-color:#22C55E; color:white; border-radius:20px; padding:12px; font-size:18px; font-weight:bold; border:none; cursor:pointer;'>💳 Перейти к оплате</button></a>", unsafe_allow_html=True)
    
    st.write("")
    st.write("📋 *После завершения перевода нажмите кнопку ниже для мгновенной генерации:*")
    
    if st.button("✅ Я оплатил(а), открыть сказку", use_container_width=True):
        if not child_name.strip():
            st.warning("Пожалуйста, сначала заполните имя ребёнка в форме выше!")
        else:
            st.session_state.payment_done = True
            st.rerun()

else:
    # Блок после подтверждения оплаты
    with st.spinner("💳 Оплата зафиксирована! Пишем уникальную сказку для вашего малыша..."):
        story_result = generate_magic_story(child_name, child_age, setting, challenge)
    
    st.write("---")
    st.markdown(f"### 📖 Персональная история для {child_name}:")
    
    with st.container(border=True):
        st.markdown(story_result)
        
    st.write("")
    st.success("✨ Сказка успешно создана! Прочитайте её ребёнку перед сном мягким, спокойным голосом.")
    
    # Сброс для нового платного заказа
    if st.button("🪄 Заказать еще одну сказку", use_container_width=True):
        st.session_state.payment_done = False
        st.rerun()

st.write("---")
st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 12px;'>MagicTales 2026. Конфиденциально и безопасно для родителей.</p>", unsafe_allow_html=True)
