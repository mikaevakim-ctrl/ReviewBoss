import streamlit as st
import requests
import json
import time

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(
    page_title="ReviewBoss | Scale Your Audience",
    page_icon="✨",
    layout="centered"
)

# --- АНИМАЦИЯ ПАДАЮЩИХ ИКОНОК НА ЗАДНЕМ ФОНЕ ---
animation_html = """
<div id="snow-container" style="position:fixed; top:0; left:0; width:100vw; height:100vh; pointer-events:none; z-index:-1; overflow:hidden; background: transparent;"></div>
<script>
const container = document.getElementById('snow-container');
const emojis = ['⭐️', '💬', '✨', '👍', '❤️', '🎬', '🍿', '🔥', '🌟', '🚀'];

function createDroplet() {
    const droplet = document.createElement('div');
    droplet.innerText = emojis[Math.floor(Math.random() * emojis.length)];
    droplet.style.position = 'absolute';
    droplet.style.top = '-50px';
    droplet.style.left = Math.random() * 100 + 'vw';
    
    const size = Math.random() * 20 + 15;
    const duration = Math.random() * 8 + 5; 
    const opacity = Math.random() * 0.35 + 0.1;
    
    droplet.style.fontSize = size + 'px';
    droplet.style.transition = `transform ${duration}s linear, opacity ${duration}s linear`;
    droplet.style.opacity = opacity;
    
    container.appendChild(droplet);
    
    setTimeout(() => {
        const drift = (Math.random() * 100 - 50);
        droplet.style.transform = `translateY(110vh) translateX(${drift}px) rotate(${Math.random() * 360}deg)`;
        droplet.style.opacity = '0';
    }, 100);
    
    setTimeout(() => {
        droplet.remove();
    }, duration * 1000 + 100);
}
setInterval(createDroplet, 600);
</script>
"""
st.components.v1.html(animation_html, height=0, width=0)

# --- УМНЫЙ ДВИЖОК КОПИРАЙТИНГА ---
def generate_response(text_input, tone, platform_type):
    api_key = st.secrets.get("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY")
    url = "https://openrouter.ai"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    target_text = text_input.strip()
    
    # Защита от ввода ссылок
    if "http://" in target_text or "https://" in target_text or "www." in target_text:
        return "⚠️ Please paste the plain text of the review or comment. Direct links are restricted due to platform firewalls."

    # Настройка инструкций под платформу
    if platform_type == "Google Maps / Yelp / TripAdvisor":
        system_instruction = (
            f"You are the elite head of communications and brand reputation for a top-tier business. "
            f"Your task is to write a highly engaging, charismatic, and persuasive reply to a customer review. "
            f"The tone of your reply must strictly be: {tone}. "
            f"Guidelines:\n"
            f"1. Never mention that you are an AI, robot, or automated software.\n"
            f"2. Sound 100% like a passionate, caring human business owner or manager.\n"
            f"3. Keep the reply concise (2-4 sentences), highly professional, and natural.\n"
            f"4. If negative, be polite and resolve the issue gracefully. If positive, express deep gratitude."
        )
    else:
        system_instruction = (
            f"You are a charismatic, high-energy YouTube Creator and influencer. "
            f"Your task is to reply to a fan comment under your latest video to maximize community engagement. "
            f"The tone of your reply must strictly be: {tone}. "
            f"Guidelines:\n"
            f"1. Never mention AI, LLMs, or automation. Sound exactly like a busy but friendly video creator.\n"
            f"2. Be catchy, conversational, and use 1-2 native emojis naturally (e.g., 🔥, 🙌, 🚀).\n"
            f"3. Keep it short (1-3 sentences) to maintain high readability in the comment section."
        )
    
    data = {
        "model": "google/gemini-2.5-flash:free",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Target text to reply to: '{target_text}'"}
        ]
    }
    
    if api_key == "YOUR_OPENROUTER_API_KEY":
        time.sleep(1.5)
        return f"[DEMO MODE] Charismatic {tone} response to: \"{target_text}\""
        
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=15)
        if response.status_code == 200:
            result = response.json()
            return result['choices']['message']['content'].strip()
        else:
            return f"System notice: Temporary high load. Status code {response.status_code}."
    except Exception:
        return "Connection timeout. Please click the button again."
# --- 1. ПЕРВЫЙ ЭКРАН (HERO SECTION) ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>Turn Reviews & Comments into Loyal Fans. In 1 Click.</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4B5563;'>Generate charismatic brand replies for Google Maps, Yelp, and YouTube in 3 seconds.</h3>", unsafe_allow_html=True)

st.write("---")

# --- 2. БЛОК С ТАРИФАМИ (PRICING) НАВЕРХУ ---
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
        st.subheader("Starter Pack")
        st.markdown("## $39/mo")
        st.write("• 300 ready replies")
        st.write("• Maps & YouTube engines")
        st.button("Get Starter", key="btn_starter", use_container_width=True)

with p_col3:
    with st.container(border=True):
        st.subheader("Creator Pro")
        st.markdown("## $89/mo")
        st.write("• Unlimited generations")
        st.write("• Custom slang & brand setup")
        st.button("Get Pro", key="btn_biz", type="primary", use_container_width=True)

st.write("---")

# --- 3. ИНТЕРАКТИВНЫЙ МУЛЬТИПЛАТФОРМЕННЫЙ ГЕНЕРАТОР ---
st.markdown("### ✍️ Test the Multi-Platform Generator")

platform = st.segmented_control(
    "Select Target Platform:",
    options=["Google Maps / Yelp / TripAdvisor", "YouTube Comments"],
    default="Google Maps / Yelp / TripAdvisor"
)

st.write("")

if platform == "Google Maps / Yelp / TripAdvisor":
    preset_reviews = {
        "Custom Text (Type below)": "",
        "🍕 5-Star Restaurant Review": "The pizza was absolutely amazing! Friendly staff and fast service. Will definitely come back next week.",
        "⭐️ 1-Star Hotel Review": "The room was noisy and the AC didn't work properly. Very disappointed with the service for this price."
    }
else:
    preset_reviews = {
        "Custom Text (Type below)": "",
        "🔥 Fan Praise Comment": "Man, this video editing is next level! Thanks for making this tutorial, it helped me so much with my project.",
        "🧐 Critical Comment": "The info is good but you talked too fast in the middle section. Had to slow down the playback to get it."
    }

selected_preset = st.selectbox("Choose a sample input:", list(preset_reviews.keys()))

if selected_preset != "Custom Text (Type below)":
    text_input = st.text_area("Source Text to Reply to:", value=preset_reviews[selected_preset], height=100)
else:
    placeholder_text = "Paste maps review plain text here..." if platform == "Google Maps / Yelp / TripAdvisor" else "Paste YouTube plain comment text here..."
    text_input = st.text_area("Source Text to Reply to:", placeholder=placeholder_text, height=100)

tone_choice = st.radio(
    "Select your Vibe / Tone of Voice:",
    ["Friendly", "Professional", "Witty"],
    horizontal=True
)

if st.button("Generate Smart Reply ✨", type="primary", use_container_width=True):
    if not text_input.strip():
        st.warning("Please enter or select some text first!")
    else:
        with st.spinner("Crafting your charismatic response..."):
            result_text = generate_response(text_input, tone_choice, platform)
        
        st.success("Done! Your response is ready to copy:")
        st.code(result_text, language="text")
        
        if platform == "Google Maps / Yelp / TripAdvisor":
            st.info("💡 Pro Tip: Fast responses boost your Local SEO maps discovery rank instantly.")
        else:
            st.info("💡 Pro Tip: Replying within 15 minutes triggers YouTube's algorithm to pump your video to more feeds.")

st.write("---")

# --- 4. БЛОК БОЛИ И ПРЕИМУЩЕСТВ ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 💔 The Routine Dragging You Down")
    st.markdown("- **Wasting hours** typing back to hundreds of comments and reviews manually.")
    st.markdown("- **Killing engagement rates** because unanswered text drops your channel score.")
    st.markdown("- **Sounding dry and boring** when trying to match your brand's true voice.")

with col2:
    st.markdown("#### 🔥 Why Creators & Brands Love ReviewBoss")
    st.markdown("- **Dual-Engine Copywriting:** Instantly shifts styles between local business owner and high-energy video creator.")
    st.markdown("- **No VPN Required:** Fast, stable, cloud-based text scripting worldwide.")
    st.markdown("- **Algorithm Boost:** High response rates trigger rapid discovery on both Google and YouTube.")

st.write("---")

# --- 5. ФУТЕР ---
st.markdown("<p style='text-align: center; color: #9CA3AF;'>No credit card required for trial. ReviewBoss 2026.</p>", unsafe_allow_html=True)
