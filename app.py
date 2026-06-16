import streamlit as st
import time

# Настройка страницы
st.set_page_config(
    page_title="ReviewBoss | Turn Reviews into Sales",
    page_icon="✨",
    layout="centered"
)

# Функция-заглушка для генерации ответа (сюда вставляется твой API-запрос)
def generate_review_reply(review_text, tone):
    # Имитируем реальную логику копирайтера без упоминания ИИ
    replies = {
        "Friendly": f"Hi there! Thank you so much for the feedback. We are thrilled you enjoyed it! Looking forward to your next visit! ✨",
        "Professional": f"Thank you for taking the time to share your experience. Your feedback is highly appreciated and helps us maintain our high standards. Best regards, Management.",
        "Witty": f"Wow, you just made our day! Thanks for the awesome words. We promise to keep being this awesome next time too! 😎"
    }
    # Имитация задержки генерации текста
    time.sleep(1.5)
    return replies.get(tone, replies["Friendly"])

# --- 1. HERO SECTION ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>Turn Maps Reviews into Loyal Customers. In 1 Click. No VPN.</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4B5563;'>Generate charismatic, high-converting brand replies for Google Maps, Yelp, and TripAdvisor in 3 seconds.</h3>", unsafe_allow_html=True)

st.write("---")

# --- 2. INTERACTIVE GENERATOR ---
st.markdown("### ✍️ Test the Smart Reply Generator")
st.write("Pick a real client review or type your own to see how it instantly transforms into a charismatic copy:")

# Готовые пресеты для демонстрации клиенту
preset_reviews = {
    "Custom Text (Type below)": "",
    "🍕 5-Star Restaurant Review": "The pizza was absolutely amazing! Friendly staff and fast service. Will definitely come back next week.",
    "⭐️ 1-Star Hotel Review": "The room was noisy and the AC didn't work properly. Very disappointed with the service for this price."
}

selected_preset = st.selectbox("Choose a sample review:", list(preset_reviews.keys()))

# Поле ввода текста
if selected_preset != "Custom Text (Type below)":
    review_input = st.text_area("Client Review Text:", value=preset_reviews[selected_preset], height=100)
else:
    review_input = st.text_area("Client Review Text:", placeholder="Paste your client's review here...", height=100)

# Выбор тональности бренда
tone_choice = st.radio(
    "Select your Brand Tone of Voice:",
    ["Friendly", "Professional", "Witty"],
    horizontal=True
)

# Логика генерации текста
if st.button("Generate Smart Reply ✨", type="primary", use_container_width=True):
    if not review_input.strip():
        st.warning("Please enter or select a review first!")
    else:
        with st.spinner("Crafting your charismatic response..."):
            result_text = generate_review_reply(review_input, tone_choice)
        
        st.success("Done! Your brand response is ready to copy:")
        st.code(result_text, language="text")
        st.info("💡 Pro Tip: Fast and engaging replies like this boost your Google Maps local SEO ranking instantly.")

st.write("---")

# --- 3. THE PROBLEM & WHY US ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 💔 The Routine Dragging You Down")
    st.markdown("- **Wasting hours** staring at a blank screen trying to find words.")
    st.markdown("- **Losing local rankings** due to slow or ignored customer feedback.")
    st.markdown("- **Sounding dry and boring** like a rigid corporate machine.")

with col2:
    st.markdown("#### 🔥 Why Local Businesses Love ReviewBoss")
    st.markdown("- **Charismatic Copywriting:** Scripts instantly adapt to your specific business vibe.")
    st.markdown("- **No VPN Required:** Runs lightning-fast and stable from anywhere in the world.")
    st.markdown("- **Google Search Boost:** Consistent text updates signal activity to search algorithms.")

st.write("---")

# --- 4. PRICING ---
st.markdown("<h3 style='text-align: center;'>Simple, Transparent Pricing</h3>", unsafe_allow_html=True)

p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    st.subheader("Free Trial")
    st.markdown("## $0")
    st.write("• 10 free text generations")
    st.write("• Core writing styles")
    st.button("Start Free", key="btn_free", use_container_width=True)

with p_col2:
    st.subheader("Starter")
    st.markdown("## $29/mo")
    st.write("• Up to 200 ready replies")
    st.write("• All writing styles")
    st.button("Get Starter", key="btn_starter", use_container_width=True)

with p_col3:
    st.subheader("Business")
    st.markdown("## $79/mo")
    st.write("• Unlimited generations")
    st.write("• Custom brand setup")
    st.button("Get Business", key="btn_biz", type="primary", use_container_width=True)

st.write("---")

# --- 5. FOOTER ---
st.markdown("<p style='text-align: center; color: #9CA3AF;'>No credit card required for trial. Setup takes 30 seconds. ReviewBoss 2026.</p>", unsafe_allow_html=True)
