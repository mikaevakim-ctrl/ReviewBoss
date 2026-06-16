import streamlit as st
import requests
import json
import time

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(
    page_title="ReviewBoss | Turn Reviews into Sales",
    page_icon="✨",
    layout="centered"
)

# --- ДВИЖОК КОПИРАЙТИНГА ---
def generate_review_reply(review_text, tone):
    api_key = st.secrets.get("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY")
    url = "https://openrouter.ai"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    system_instruction = (
        f"You are the elite head of communications and brand reputation for a top-tier business. "
        f"Your task is to write a highly engaging, charismatic, and persuasive reply to a customer review. "
        f"The tone of your reply must strictly be: {tone}. "
        f"Guidelines:\n"
        f"1. Never mention that you are an AI, robot, or automated software.\n"
        f"2. Sound 100% like a passionate, caring human business owner or manager.\n"
        f"3. Keep the reply concise (2-4 sentences), highly professional, and natural.\n"
        f"4. If the review is negative, be extremely polite, resolve the issue gracefully, and invite them back to fix it.\n"
        f"5. If the review is positive, express deep gratitude and build excitement for their next visit.\n"
        f"6. Optimize the text subtly for local maps discovery without sounding spammy."
    )
    
    data = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Here is the customer review to reply to: '{review_text}'"}
        ]
    }
    
    if api_key == "YOUR_OPENROUTER_API_KEY":
        time.sleep(1.5)
        replies = {
            "Friendly": "Hi there! Thank you so much for the feedback. We are thrilled you enjoyed your experience! Looking forward to your next visit! ✨",
            "Professional": "Thank you for taking the time to share your experience. Your feedback is highly appreciated and helps us maintain our high standards. Best regards, Management.",
            "Witty": "Wow, you just made our day! Thanks for the awesome words. We promise to keep being this awesome next time too! 😎"
        }
        return replies.get(tone, replies["Friendly"])
        
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=12)
        if response.status_code == 200:
            result = response.json()
            return result['choices']['message']['content'].strip()
        else:
            return f"System notice: Temporary high load. Output generated in fallback mode."
    except Exception:
        return "Connection timeout. Please click the button again."


# --- 1. ПЕРВЫЙ ЭКРАН (HERO SECTION) ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>Turn Maps Reviews into Loyal Customers. In 1 Click. No VPN.</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4B5563;'>Generate charismatic, high-converting brand replies for Google Maps, Yelp, and TripAdvisor in 3 seconds.</h3>", unsafe_allow_html=True)

st.write("---")


# --- 2. БЛОК С ТАРИФАМИ (PRICING) В КРАСИВЫХ РАМКАХ ---
st.markdown("<h3 style='text-align: center; color: #1F2937;'>Choose Your Growth Plan</h3>", unsafe_allow_html=True)

p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    with st.container(border=True):
        st.subheader("Free Trial")
        st.markdown("## $0")
        st.write("• 3 free text generations")
        st.write("• Core writing styles")
        st.button("Start Free", key="btn_free", use_container_width=True)

with p_col2:
    with st.container(border=True):
        st.subheader("Starter")
        st.markdown("## $29/mo")
        st.write("• Up to 200 ready replies")
        st.write("• All writing styles")
        st.button("Get Starter", key="btn_starter", use_container_width=True)

with p_col3:
    with st.container(border=True):
        st.subheader("Business")
        st.markdown("## $79/mo")
        st.write("• Unlimited generations")
        st.write("• Custom brand setup")
        st.button("Get Business", key="btn_biz", type="primary", use_container_width=True)

st.write("---")


# --- 3. ГЛАВНЫЙ БЛОК: ГЕНЕРАТОР СЛЕВА, ТЕКСТ СПРАВА ---
main_col1, main_col2 = st.columns([1.2, 1.0], gap="large")

# ЛЕВАЯ КОЛОНКА: ИНТЕРАКТИВНЫЙ ГЕНЕРАТОР
with main_col1:
    st.markdown("### ✍️ Test the Smart Reply Generator")
    st.write("Pick a sample review or type your own:")

    preset_reviews = {
        "Custom Text (Type below)": "",
        "🍕 5-Star Restaurant Review": "The pizza was absolutely amazing! Friendly staff and fast service. Will definitely come back next week.",
        "⭐️ 1-Star Hotel Review": "The room was noisy and the AC didn't work properly. Very disappointed with the service for this price."
    }

    selected_preset = st.selectbox("Choose a sample review:", list(preset_reviews.keys()))

    if selected_preset != "Custom Text (Type below)":
        review_input = st.text_area("Client Review Text:", value=preset_reviews[selected_preset], height=100)
    else:
        review_input = st.text_area("Client Review Text:", placeholder="Paste your client's review here...", height=100)

    tone_choice = st.radio(
        "Select your Brand Tone of Voice:",
        ["Friendly", "Professional", "Witty"],
        horizontal=True
    )

    if st.button("Generate Smart Reply ✨", type="primary", use_container_width=True):
        if not review_input.strip():
            st.warning("Please enter or select a review first!")
        else:
            with st.spinner("Crafting your charismatic response..."):
                result_text = generate_review_reply(review_input, tone_choice)
            
            st.success("Done! Your brand response is ready to copy:")
            st.code(result_text, language="text")

# ПРАВАЯ КОЛОНКА: РУТИНА И ПРЕИМУЩЕСТВА (СТРОКИ С БОКОВ)
with main_col2:
    st.write("##") # Небольшой отступ сверху для выравнивания
    st.markdown("#### 💔 The Routine Dragging You Down")
    st.markdown("- **Wasting hours** staring at a blank screen trying to find the right words.")
    st.markdown("- **Losing local rankings** in search maps due to slow or ignored feedback.")
    st.markdown("- **Sounding dry and boring** like a rigid, outdated corporate machine.")
    
    st.write("") # Разделительный отступ между блоками
    
    st.markdown("#### 🔥 Why Local Businesses Love ReviewBoss")
    st.markdown("- **Charismatic Copywriting:** Scripts instantly adapt to your specific business vibe.")
    st.markdown("- **No VPN Required:** Runs lightning-fast and stable from anywhere in the world.")
    st.markdown("- **Google Search Boost:** Consistent text updates signal activity to search algorithms.")

st.write("---")


# --- 4. ФУТЕР ---
st.markdown("<p style='text-align: center; color: #9CA3AF;'>No credit card required for trial. Setup takes 30 seconds. ReviewBoss 2026.</p>", unsafe_allow_html=True)

