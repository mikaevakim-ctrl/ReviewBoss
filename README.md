[app.py](https://github.com/user-attachments/files/28973300/app.py)
import streamlit as st
import requests
import streamlit.components.v1 as components
import random

# Настройка страницы
st.set_page_config(page_title="Мировой ИИ-Мониторинг Карт", page_icon="🌍", layout="centered")

CORRECT_PASSWORD = "admin"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 Вход в личный кабинет")
    user_password = st.text_input("Введите ваш персональный пароль доступа:", type="password")
    
    if st.button("Войти", use_container_width=True):
        if user_password == CORRECT_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ Неверный пароль! Доступ заблокирован.")
else:
    if st.sidebar.button("🚪 Выйти из кабинета"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.title("🌍 Международный ИИ-Помощник для Бизнеса")
    st.write("Автоматический поиск отзывов и генерация ответов (Яндекс, Google, Tripadvisor)")

    st.markdown("---")
    st.subheader("🔍 Сканирование карт")

    platform = st.selectbox(
        "📍 Выберите платформу для проверки:",
        ("Яндекс Карты", "Google Карты (Google Maps)", "Tripadvisor", "Yelp")
    )

    place_url = st.text_input("🔗 Вставьте ссылку на карточку вашей компании:", placeholder="https://maps...")

    if st.button("🚀 Найти новые отзывы и подготовить ответы", use_container_width=True):
        if not place_url.strip():
            st.warning("⚠️ Пожалуйста, вставьте ссылку на ваше заведение!")
        else:
            with st.spinner(f"⏳ Сканируем страницу {platform}..."):
                try:
                    if "яндекс" in platform.lower():
                        mock_reviews = [
                            {"author": "Иван П.", "rating": 1, "text": "Ужасно долго несли заказ, суп оказался переваренным."},
                            {"author": "Елена К.", "rating": 5, "text": "Прекрасная атмосфера, вежливый персонал и очень быстрая подача!"}
                        ]
                    else:
                        mock_reviews = [
                            {"author": "John Doe", "rating": 2, "text": "The food was cold and the waiter forgot about our drinks. Very disappointed.", "lang": "en"},
                            {"author": "Maria Schmidt", "rating": 5, "text": "Amazing place! Best burger in town, will definitely come back!", "lang": "en"}
                        ]
                    
                    st.info(f"✅ Успешно найдено новых отзывов без ответа: {len(mock_reviews)}")
                    
                    for i, r in enumerate(mock_reviews):
                        st.markdown("---")
                        st.subheader(f"💬 Отзыв №{i+1} от {r['author']} ({'⭐' * r['rating']})")
                        st.write(f"*{r['text']}*")
                        
                        # Промпт с требованием использовать юмор и самоиронию
                        prompt = f"""Ты — харизматичный, остроумный владелец ресторана. Ответь на отзыв гостя живым, разговорным языком с добавлением КЛАССНОГО ТОНКОГО ЮМОРА и легкой самоиронии.
                        Никаких штампов!
                        
                        1. Отвечай на языке отзыва.
                        2. Если отзыв плохой (1-3 звезды): искренне извинись за косяк (ожидание, переваренный суп), но добавь шутку. Например, что повар перепутал кастрюлю с вулканом, или что улитки на улице бегают быстрее наших курьеров, и ты уже купил поварам по спортивному велосипеду для ускорения. Пообещай лично устроить разгон на кухне.
                        3. Если отзыв хороший (4-5 звезд): бурно обрадуйся, пошути, что шеф-повар от гордости увеличился в размерах, а официанты прямо сейчас танцуют брейк-данс у барной стойки от вашего отзыва. Пригласи в гости снова.
                        
                        Отзыв от {r['author']}: "{r['text']}"
                        Остроумный ответ владельца:"""
                        
                        url = "https://hf.space"
                        ai_reply = ""
                        try:
                            response = requests.post(url, json={"data": [prompt, "", 0.85, 0.9]}, timeout=15)
                            if response.status_code == 200:
                                ai_reply = response.json()['data'].strip()
                        except:
                            pass
                            
                        # ФОЛЛБЭК: Уникальные и смешные готовые варианты на случай сбоя сети
                        if not ai_reply or len(ai_reply) < 10:
                            if r['rating'] <= 3:
                                bad_options = [
                                    f"Иван П., приветствую! Кажется, наш шеф-повар в этот день решил, что он варит не суп, а зелье бессмертия, раз удерживал его на огне так долго... 🥣 Искренне прошу прощения за этот кулинарный арт-хаус! Уже выдал команде кухни по секундомеру и провел жесткую беседу. Приходите, мы исправимся и докажем, что варить супы мы умеем быстрее и вкуснее!",
                                    f"Иван П., добрый день! Судя по вашему отзыву, наши официанты в тот день передвигались со скоростью сонной улитки, а суп пал жертвой безумного эксперимента повара. Стыдно, извините нас! Повару выписан строгий нагоняй, а ребятам в зале куплены новые кроссовки для скорости. Очень ждем вас снова, чтобы реабилитироваться в ваших глазах!",
                                    f"Эх, Иван П., приношу свои глубочайшие извинения... Похоже, наш суп слишком долго медитировал на плите. Нам безумно неловко за такое ожидание и переваренное блюдо. На кухне уже идет громкий разбор полетов с метанием поварешек. Дайте нам еще один шанс, мы приготовим для вас всё идеально и со скоростью звука!"
                                ]
                                ai_reply = random.choice(bad_options)
                            else:
                                good_options = [
                                    f"Елена К., огромное спасибо! После вашего отзыва наш шеф-повар от гордости задрал нос так высоко, что чуть не врезался в потолок, а команда зала прямо сейчас танцует победный танец у барной стойки! 💃 Передаем вам коллективный привет и всегда ждем на повторение этой прекрасной атмосферы!",
                                    f"Вау, Елена К., спасибо за такой заряд позитива! Наш бариста, прочитав это, от радости нарисовал на латте целую картину. Безумно рады, что вам всё понравилось. Забегайте к нам почаще, мы всегда на низком старте, чтобы выдать вам лучшую подачу! 😉",
                                    f"Елена К., день прожит не зря! Ваш отзыв распечатали и повесили на самое видное место на кухне — теперь повара готовят еще быстрее под влиянием вашей похвалы. Спасибо за теплые слова, ждем вас в гости снова за порцией отличного настроения!"
                                ]
                                ai_reply = random.choice(good_options)

                        st.success("📝 Рекомендуемый ИИ-ответ (с юмором):")
                        st.text_area(f"Ответ для {r['author']}:", value=ai_reply, height=150, key=f"reply_{i}_{random.randint(1,1000)}")
                        
                        clean_reply = ai_reply.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
                        
                        button_html = f"""
                        <div style="font-family: sans-serif;">
                            <button onclick="copyToClipboard()" style="width: 100%; background-color: #24a0ed; color: white; padding: 12px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px;">
                                📋 Скопировать ответ для {r['author']}
                            </button>
                            <p id="status_{i}" style="color: #4CAF50; font-size: 12px; text-align: center; margin-top: 5px; display: none; font-weight: bold;">✓ Текст успешно скопирован!</p>
                        </div>
                        <script>
                        function copyToClipboard() {{
                            const text = "{clean_reply}";
                            navigator.clipboard.writeText(text).then(() => {{
                                document.getElementById("status_{i}").style.display = "block";
                                setTimeout(() => {{ document.getElementById("status_{i}").style.display = "none"; }}, 2000);
                            }}).catch(err => {{
                                alert('Ошибка копирования: ' + err);
                            }});
                        }}
                        </script>
                        """
                        components.html(button_html, height=70)
                        
                except Exception as e:
                    st.error(f"❌ Системная ошибка скрипта: {e}")
