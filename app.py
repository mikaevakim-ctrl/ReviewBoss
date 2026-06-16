def generate_response(text_input, tone, platform_type):
    api_key = st.secrets.get("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY")
    url = "https://openrouter.ai"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    target_text = text_input.strip()
    
    # ЕСЛИ ВЫБРАНЫ КАРТЫ: Блокируем ссылки, так как карты защищены, требуем текст отзыва
    if platform_type == "Google Maps / Yelp / TripAdvisor":
        if "http://" in target_text or "https://" in target_text:
            return "⚠️ Security Notice: Maps platforms require direct text input due to security firewalls. Please copy and paste the plain review text here."
    
    # ЕСЛИ ВЫБРАН YOUTUBE: Включаем авто-скачивание по ссылке
    else:
        if "://youtube.com" in target_text or "youtu.be/" in target_text:
            try:
                downloader = YoutubeCommentDownloader()
                comments = downloader.get_comments_from_url(target_text, sort_by=SORT_BY_RECENT)
                first_comment = next(comments, None)
                
                if first_comment and 'text' in first_comment:
                    target_text = first_comment['text']
                    st.toast(f"📥 Successfully fetched latest comment: \"{target_text[:40]}...\"")
                else:
                    return "Error: No public comments found on this YouTube video."
            except Exception:
                return "Error: Could not extract comments from this URL. Make sure the video is public."
        elif "http://" in target_text or "https://" in target_text:
            return "⚠️ Please paste a valid YouTube video link or type a plain comment."

    # Формирование промптов для стабильной модели Google Gemini
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
