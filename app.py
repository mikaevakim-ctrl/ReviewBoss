import streamlit as st
import requests
import json
import time

# --- НАСТРОЙКА СТРАНИЦЫ (Премиальный детский стиль) ---
st.set_page_config(
    page_title="MagicTales | Personalized Therapy Stories",
    page_icon="🔮",
    layout="centered"
)

# Изменяем стиль шрифтов и кнопок, чтобы сайт выглядел как дорогая книга
st.markdown("""
<style>
    .stApp {
        background-color: #FAFAFC;
    }
    h1, h2, h3 {
        font-family: 'Cozy', 'Comic Sans MS', sans-serif !important;
    }
    div.stButton > button:first-child {
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

# --- АНИМАЦИЯ ПАДАЮЩИХ ВОЛШЕБНЫХ ЗВЕЗД (Мягкая, не отвлекает от чтения) ---
animation_html = """
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
"""
st.components.v1.html(animation_html, height=0, width=0)

# --- БЕСПЛАТНЫЙ ДВИЖОК ГЕНЕРАЦИИ СКАЗОК ---
def generate_magic_story(child_name, child_age, setting, challenge):
    api_key = st.secrets.get("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY")
    url = "https://openrouter.ai"
    
    # Режим авто-генерации (заглушка), если ключ не подключен
    if api_key == "YOUR_OPENROUTER_API_KEY" or len(api_key) < 10:
        time.sleep(1.2)
        return (
            f"✨ **Давным-давно, в одном удивительном месте под названием {setting}...** ✨\n\n"
            f"Жил-был очень смелый и добрый ребёнок, которого звали **{child_name}**. Ему было ровно {child_age} лет. "
            f"{child_name} больше всего на свете любил исследовать мир вокруг, но иногда он сталкивался с небольшой трудностью: *{challenge.lower()}*.\n\n"
            f"Однажды вечером, маленькая волшебная фея прилетела к его окошку, присела на край подушки и прошептала: "
            f"«{child_name}, вся самая сильная магия уже находится внутри твоего доброго сердца! Ты гораздо сильнее и смелее, чем тебе кажется».\n\n"
            f"С той самой ночи {child_name} сладко засыпал с улыбкой на лице, зная, что со всеми трудностями он обязательно справится. Конец волшебной сказки. 🌙"
        )
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Профессиональная инструкция для детского психолога-сказочника
    system_instruction = (
        "You are a compassionate child psychologist and a master storyteller for kids. "
        "Your goal is to write a warm, beautifully structured therapeutic bedtime story based on the user's inputs. "
        "The story MUST be written in the same language as the child's name provided (If Russian name -> write in Russian, if English name -> write in English). "
        "Rules:\n"
        "1. Never use technical, AI, or corporate words. Sound 100% like a loving human writer.\n"
        "2. Make the child the main character who gracefully learns a lesson or overcomes a fear through a gentle metaphor.\n"
        "3. The story must feel deeply safe, cozy, comforting, and have a beautiful happy ending.\n"
        "4. Keep it concise but magical (approx. 250-400 words), ideal for reading aloud before bed."
    )
    
    user_content = (
        f"Write a cozy bedtime story for a child named {child_name}, age {child_age}. "
        f"The story takes place in: {setting}. "
        f"The theme to gently guide the child through is: {challenge}."
    )
    
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
            return "Ой, волшебная книга закрылась от сильного ветра. Пожалуйста, нажмите кнопку создания еще раз! 🪄"
    except Exception:
        return "Сказочная пыль еще укладывается. Пожалуйста, попробуйте нажать кнопку еще один раз!"
# --- 1. КРАСИВЫЙ ЗАГОЛОВОК САЙТА ---
st.markdown("<h1 style='text-align: center; color: #4F46E5; margin-bottom: 0;'>🔮 MagicTales</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4B5563; font-size: 18px; margin-top: 5px;'>Создайте уникальную терапевтическую сказку для вашего малыша</p>", unsafe_allow_html=True)

st.write("")

# --- 2. ПРОСТАЯ И ПОНЯТНАЯ ФОРМА ВВОДА ---
# Оборачиваем форму в рамку, чтобы она смотрелась аккуратно
with st.container(border=True):
    st.markdown("##### 📝 Заполните всего 4 простых поля:")
    
    child_name = st.text_input("Как зовут вашего ребёнка?", placeholder="Например: Лео, София, Максим", max_chars=20)
    
    child_age = st.slider("Сколько лет вашему малышу?", min_value=2, max_value=10, value=5)
    
    setting = st.selectbox(
        "Где будет происходить действие сказки?",
        ["В затерянном волшебном лесу", "На далекой космической станции", "В секретном подводном королевстве", "В уютном замке на мягком облаке", "В долине добрых динозавров"]
    )
    
    challenge = st.selectbox(
        "Какую тему или каприз мы хотим мягко решить?",
        [
            "Боязнь темноты и ночных монстров", 
            "Нежелание ложиться спать вовремя", 
            "Неумение делиться своими игрушками", 
            "Сложная адаптация и страх перед детским садиком",
            "Частые вспышки злости, обиды или капризы"
        ]
    )

st.write("")

# Кнопка запуска
if st.button("Создать волшебную сказку ✨", use_container_width=True):
    if not child_name.strip():
        st.warning("Пожалуйста, введите имя вашего ребёнка, чтобы сказка получилась персональной!")
    else:
        with st.spinner("Собираем волшебную пыль и пишем вашу сказку..."):
            story_result = generate_magic_story(child_name, child_age, setting, challenge)
        
        st.write("---")
        st.markdown(f"### 📖 Ваша персональная история для {child_name}:")
        
        # Выводим сказку в красивом, чистом текстовом блоке без программного кода
        with st.container(border=True):
            st.markdown(story_result)
            
        st.write("")
        st.success("✨ Готово! Прочитайте эту сказку вашему ребёнку сегодня перед сном спокойным, мягким голосом.")

st.write("---")
st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 12px;'>MagicTales 2026. Сделано с любовью для заботливых родителей.</p>", unsafe_allow_html=True)
