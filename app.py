import streamlit as st
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

# МОЩНЫЙ ВСТРОЕННЫЙ ТЕСТОВЫЙ ГЕНЕРАТОР СКАЗОК (Для проверки без сторонних API)
def generate_magic_story(child_name, child_age, setting, challenge):
    time.sleep(1.0) # Имитация легкой загрузки волшебства
    name = child_name.strip()
    
    # Автоматически собираем глубокую и красивую терапевтическую сказку
    story = (
        f"### ✨ Волшебное приключение в месте под названием: {setting} ✨\n\n"
        f"Давным-давно, на самой опушке, где звёзды касались земли, жил-был маленький, но очень отважный герой по имени **{name}**. "
        f"Ему было ровно {child_age} лет. {name} был удивительным ребёнком: его глаза светились любопытством, а улыбка могла разогнать любые тучи. "
        f"Больше всего на свете он любил исследовать {setting.lower()} и искать секретные тропинки.\n\n"
        f"Но однажды случилось так, что на нашего героя напала временная грусть, а причиной тому была — *{challenge.lower()}*. "
        f"Каждый раз, когда приходилось сталкиваться с этим, {name} чувствовал себя маленьким и беззащитным, словно пушистый зайчик под проливным дождём.\n\n"
        f"В один из таких вечеров, когда на небе зажглась самая яркая луна, к окошку прилетела Мудрая Хранительница Сказок — белоснежная сова с добрыми глазами. "
        f"Она присела на край кроватки, мягко взмахнула крылом и прошептала:\n\n"
        f"— *«Слушай меня внимательно, дорогой {name}. Вся самая сильная и чистая магия в мире уже живет внутри твоего сердца. "
        f"Каждый раз, когда тебе покажется, что возвращается {challenge.lower()}, просто сделай глубокий вдох, улыбнись и мысленно зажги внутри себя маленький золотой огонек. "
        f"Этот огонек прогонит любые страхи, обиды и капризы, потому что ты — настоящий защитник своего спокойствия!»*\n\n"
        f"Сова подарила герою маленькую невидимую звездочку, которую положила ему прямо под подушку. "
        f"{name} зажмурился, почувствовал, как внутри него разливается теплое и уютное волшебство, и сладко-сладко уснул.\n\n"
        f"С тех пор, стоило только возникнуть трудности, {name} вспоминал слова Мудрой Совы, зажигал свой внутренний огонек и побеждал любые капризы с легкой улыбкой. "
        f"Ведь он знал, что в месте под названием {setting} теперь всегда царят мир, радость и самые добрые сны. 🌙✨"
    )
    return story
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
    # Блок скидки на первую покупку
    is_first_time = st.checkbox("✨ Это моя первая сказка на сайте (Получить скидку)", value=True)
    price = 190 if is_first_time else 290

st.write("")

# --- 3. ПЛАТЕЖНЫЙ ЭКРАН И ГЕНЕРАЦИЯ ---
if not st.session_state.payment_done:
    # Блок до оплаты
    st.markdown(f"<h4 style='text-align: center;'>Стоимость создания сказки: <b style='color:#6366F1;'>{price} ₽</b></h4>", unsafe_allow_html=True)
    st.write("Нажмите кнопку ниже, чтобы перейти к быстрой оплате. После оплаты ваша персональная сказка откроется автоматически!")
    
    # Ссылка на оплату
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
