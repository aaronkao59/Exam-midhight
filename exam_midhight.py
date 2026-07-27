import streamlit as st
import random
import json
import os

APP_VERSION = "v3.1.1 (Image Path Decoupled)"

# --- 1. 配置頁面與自定義主題 (黑/冷金/淡紫) ---
# initial_sidebar_state="collapsed" 保留原設定
st.set_page_config(
    page_title="中高級認證",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 定義配色常量
COLOR_GOLD_LIGHT = "#E1D0A3" # 冷金色 (Light)
COLOR_GOLD_DARK = "#D4AF37"  # 奢華金 (Dark)
COLOR_PURPLE = "#E6E6FA"     # 淡紫色 (Lavender)
COLOR_BLACK_BG = "#111111"    # 深黑背景
COLOR_DEEP_GRAY = "#1E1E1E"  # 卡片/側邊欄深色

# 注入 CSS 樣式
st.markdown(f"""
    <style>
    /* === 1. 全局字體與背景設置 === */
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
    }}

    /* === 2. Light Mode (淺色模式) 樣式 === */
    /* 目標是：黑金配，淡紫強調 */
    @media (prefers-color-scheme: light) {{
        [data-testid="stAppViewContainer"] {{
            background-color: #FFFFFF !important; /* 白色背景 */
            color: #111111 !important; /* 深黑文字 */
        }}
        
        /* 標題與副標題 - 冷金色 */
        h1, h2, h3, h4, h5, h6 {{
            color: {COLOR_GOLD_DARK} !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
        }}
        
        /* Quiz Card (測驗卡片) - 黑底金邊，奢華感 */
        .quiz-card {{
            background-color: {COLOR_BLACK_BG} !important;
            color: {COLOR_GOLD_LIGHT} !important;
            padding: 30px;
            border-radius: 20px;
            border: 2px solid {COLOR_GOLD_DARK};
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            margin-top: 20px;
            margin-bottom: 30px;
        }}
        .quiz-card p, .quiz-card li, .quiz-card span, .quiz-card label {{
            color: {COLOR_GOLD_LIGHT} !important;
        }}
        .quiz-card h1, .quiz-card h2, .quiz-card h3 {{
            color: #FFFFFF !important; /* 卡片內標題用白色 */
        }}

        /* Segmented Control (主選單) - 黑金淡紫 */
        div[data-testid="stSegmentedControl"] button {{
            border-color: {COLOR_GOLD_DARK} !important;
            color: {COLOR_GOLD_DARK} !important;
            background-color: transparent !important;
        }}
        div[data-testid="stSegmentedControl"] button[aria-selected="true"] {{
            background-color: {COLOR_GOLD_DARK} !important;
            color: {COLOR_BLACK_BG} !important;
            font-weight: bold !important;
        }}

        /* Radio Buttons, Checkboxes (卡片內選項) - 金色 */
        .stRadio label, .stCheckbox label {{
            color: {COLOR_GOLD_LIGHT} !important;
        }}
        div[data-testid="stMarkdownContainer"] p {{
             color: {COLOR_GOLD_LIGHT} !important;
        }}
        
        /* Buttons (按鈕) - 黑金奢華 */
        .stButton>button {{
            border-radius: 12px;
            border: 2px solid {COLOR_GOLD_DARK} !important;
            background-color: {COLOR_BLACK_BG} !important;
            color: {COLOR_GOLD_DARK} !important;
            font-weight: 600 !important;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: {COLOR_GOLD_DARK} !important;
            color: {COLOR_BLACK_BG} !important;
            transform: translateY(-2px);
        }}

        /* Expander, Alert (擴展器/警示) - 淡紫色/金色 */
        .stAlert {{
            border-radius: 15px !important;
            border: none !important;
            background-color: rgba(230, 230, 250, 0.2) !important; /* 淡紫背景 */
            color: {COLOR_GOLD_DARK} !important;
        }}
        .stExpander {{
            border: 1px solid rgba(212, 175, 55, 0.3) !important;
            border-radius: 15px !important;
            background-color: rgba(255, 255, 255, 0.5) !important;
        }}

    }}

    /* === 3. Dark Mode (深色模式) 樣式 === */
    /* 目標是：全黑底，金字金邊，淡紫強調 */
    @media (prefers-color-scheme: dark) {{
        [data-testid="stAppViewContainer"] {{
            background-color: {COLOR_BLACK_BG} !important; /* 全黑背景 */
            color: {COLOR_GOLD_LIGHT} !important; /* 冷金文字 */
        }}
        
        /* 標題與副標題 - 冷金色 */
        h1, h2, h3, h4, h5, h6 {{
            color: {COLOR_GOLD_LIGHT} !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
        }}
        
        /* Quiz Card (測驗卡片) - 深黑底金邊，奢華感 */
        .quiz-card {{
            background-color: {COLOR_DEEP_GRAY} !important;
            color: {COLOR_GOLD_LIGHT} !important;
            padding: 30px;
            border-radius: 20px;
            border: 2px solid {COLOR_GOLD_DARK};
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            margin-top: 20px;
            margin-bottom: 30px;
        }}
        
        /* Segmented Control (主選單) - 冷金淡紫 */
        div[data-testid="stSegmentedControl"] button {{
            border-color: {COLOR_GOLD_LIGHT} !important;
            color: {COLOR_GOLD_LIGHT} !important;
            background-color: transparent !important;
        }}
        div[data-testid="stSegmentedControl"] button[aria-selected="true"] {{
            background-color: {COLOR_GOLD_LIGHT} !important;
            color: {COLOR_BLACK_BG} !important;
            font-weight: bold !important;
        }}

        /* Buttons (按鈕) - 金色 */
        .stButton>button {{
            border-radius: 12px;
            border: 2px solid {COLOR_GOLD_LIGHT} !important;
            background-color: {COLOR_BLACK_BG} !important;
            color: {COLOR_GOLD_LIGHT} !important;
            font-weight: 600 !important;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: {COLOR_GOLD_LIGHT} !important;
            color: {COLOR_BLACK_BG} !important;
            transform: translateY(-2px);
        }}

        /* Expander, Alert (擴展器/警示) - 淡紫強調 */
        .stAlert {{
            border-radius: 15px !important;
            border: none !important;
            background-color: rgba(230, 230, 250, 0.1) !important; /* 淡紫背景 */
            color: {COLOR_GOLD_LIGHT} !important;
        }}
        .stExpander {{
            border: 1px solid rgba(225, 208, 163, 0.2) !important;
            border-radius: 15px !important;
            background-color: {COLOR_DEEP_GRAY} !important;
        }}
        
        /* Input & Text Area (輸入框) - 金色邊框 */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
            background-color: {COLOR_BLACK_BG} !important;
            color: {COLOR_GOLD_LIGHT} !important;
            border: 1px solid rgba(212, 175, 55, 0.5) !important;
            border-radius: 10px !important;
        }}
        
        /* Form 樣式 */
        div[data-testid="stForm"] {{
            border: none !important;
            padding: 0 !important;
        }}
    }}

    /* === 4. 其他通用微調 (保留原功能) === */
    div[data-testid="stHorizontalBlock"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}
    
    /* 滑塊、切換開關、單選按鈕 - 統一淡紫強調色 */
    .stSlider > div > div > div > div {{ background-color: {COLOR_PURPLE} !important; }}
    .stRadio input[type="radio"]:checked + div, .stCheckbox input[type="checkbox"]:checked + div {{
        background-color: {COLOR_PURPLE} !important;
        border-color: {COLOR_PURPLE} !important;
    }}
    .stToggleSwitch > div > div > div > div {{ background-color: {COLOR_PURPLE} !important; }}

    </style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_json_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

# --- 2. 數據加載與功能代碼 (保持不變) ---
# 預載入全域題庫防腐層
DB_DIALOGUE = load_json_data("data/listening_dialogue.json")
DB_SPEAKING_READ = load_json_data("data/speaking_quiz.json")
DB_SPEAKING_QA = load_json_data("data/speaking_situations.json")
DB_SPEAKING_IMG = load_json_data("data/speaking_images.json")
DB_READING = load_json_data("data/reading_quiz.json")
DB_WRITING = load_json_data("data/writing_quiz.json")

QUIZ_DATA_WORDS = [
    {"id": 1, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-01.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["riyar", "'alo", "fanaw", "sa'owac"], "correct_text": "riyar"},
    {"id": 2, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-02.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["korkor", "rohayan", "romakat", "rotarot"], "correct_text": "romakat"},
    {"id": 3, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-03.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["hadhad", "hakhak", "hawan", "hafay"], "correct_text": "hafay"},
    {"id": 4, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-04.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["tefo'", "'okoy", "tafokod", "tafolod"], "correct_text": "tafokod"},
    {"id": 5, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-05.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["fakar", "tayhi", "pitaw", "tarakar"], "correct_text": "pitaw"}
]

# --- 3. UI 主體與邏輯 (保持不變) ---
st.title("🎓 中高級認證")
st.caption("[請選擇練習平台]")

main_options = ["📋 認證考試說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
current_tab = st.segmented_control("主選單導覽", main_options, default=None, label_visibility="collapsed")

if current_tab == "📋 認證考試說明":
    st.subheader("📋 認證考試說明")
    st.divider()
    with st.expander("1. 詞彙範圍/參考教材", expanded=False):
        st.markdown("* **詞彙範圍：** 學習詞表1至800詞，以及其衍生詞。\n* **參考教材：** 包含（第1階至第9階）教材、生活會話篇、閱讀書寫篇。")
    with st.expander("2. 測驗架構/題型配分", expanded=False):
        st.caption("中高級認證總分為100分，[聽力(20分)/口說(30分)/閱讀(30分)/寫作(20分)四個項目]")
        st.markdown("* **聽力測驗** (聽音選詞, 對話理解)\n* **口說測驗** (段落朗讀, 情境問答, 看圖表達)\n* **閱讀測驗** (詞彙語意, 語言結構)\n* **寫作測驗** (句子聽寫, 問答題)")
    with st.expander("3. 合格標準", expanded=False):
        st.markdown("總分達60分以上，且單項成績達聽力15分、口說15分、閱讀18分、寫作12分以上。")

elif current_tab == "🎧 聽力":
    st.subheader("🎧 聽力測驗 (pitengil)")
    st.divider()
    sub_tab = st.radio("題型選擇：", ["選擇題-聽音選詞", "選擇題-對話理解"], horizontal=True)
    
    if sub_tab == "選擇題-聽音選詞":
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        
        # 🛡️ 狀態解耦防禦
        if "lw_ptr" not in st.session_state: 
            st.session_state.lw_ptr = 0
        if "lw_order" not in st.session_state or len(st.session_state.lw_order) != len(QUIZ_DATA_WORDS):
            st.session_state.lw_order = list(range(len(QUIZ_DATA_WORDS)))
            random.shuffle(st.session_state.lw_order)
            
        ptr = st.session_state.lw_ptr
        if ptr < len(QUIZ_DATA_WORDS):
            quiz = QUIZ_DATA_WORDS[st.session_state.lw_order[ptr]]
            st.write(f"**[當前進度：第 {ptr + 1} 題 / 共 {len(QUIZ_DATA_WORDS)} 題]**")
            st.write(quiz["question_text"])
            
            if os.path.exists(quiz["audio_path"]):
                st.audio(quiz["audio_path"], format="audio/mp3")
            else:
                st.warning(f"⚠️ 找不到音檔：`{quiz['audio_path']}`")
                
            with st.form(key=f"lw_form_{ptr}"):
                opts = quiz["options"].copy()
                if f"lw_opts_{ptr}" not in st.session_state:
                    random.shuffle(opts)
                    st.session_state[f"lw_opts_{ptr}"] = opts
                
                choice = st.radio("答案選項：", st.session_state[f"lw_opts_{ptr}"], index=None)
                submit = st.form_submit_button("📥 提交答案")
                
                if submit:
                    if choice == quiz["correct_text"]:
                        st.success(f"✓ Fangcal! 正確答案：**{quiz['correct_text']}**")
                    else:
                        st.error(f"✕ 再接再厲！正確答案：**{quiz['correct_text']}**")
            
            if st.button("➡️ 下一題", key=f"lw_next_{ptr}"):
                st.session_state.lw_ptr += 1
                st.rerun()
        else:
            st.success("🎉 您已完成本輪挑戰！")
            if st.button("🔄 重新挑戰"):
                st.session_state.lw_ptr = 0
                random.shuffle(st.session_state.lw_order)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif sub_tab == "選擇題-對話理解":
        if not DB_DIALOGUE:
            st.error("📭 題庫建置中或檔案遺失 (listening_dialogue.json)")
        else:
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            mode = st.radio("選題模式：", ["隨機挑題", "自主選題"], horizontal=True)
            
            # 🛡️ 狀態解耦防禦
            if "ld_ptr" not in st.session_state:
                st.session_state.ld_ptr = 0
            if "ld_order" not in st.session_state or len(st.session_state.ld_order) != len(DB_DIALOGUE):
                st.session_state.ld_order = list(range(len(DB_DIALOGUE)))
                random.shuffle(st.session_state.ld_order)
                
            q_idx = st.session_state.ld_order[st.session_state.ld_ptr] if mode == "隨機挑題" else st.selectbox("指定題組：", range(len(DB_DIALOGUE)), format_func=lambda x: f"第 {x+1} 題")
            
            if st.session_state.ld_ptr < len(DB_DIALOGUE) or mode == "自主選題":
                quiz = DB_DIALOGUE[q_idx]
                st.write(f"**[當前練習：第 {q_idx + 1} 題]**")
                
                audio_path = f"assets/audio/01_listening/listening_dialogue/dialogue_{str(quiz.get('quiz_id', q_idx)).zfill(2)}.mp3"
                if os.path.exists(audio_path):
                    st.audio(audio_path, format="audio/mp3")
                else:
                    st.info("💡 音檔製作中")
                
                if st.toggle("👁️ 顯示對話文字", key=f"ld_txt_{q_idx}"):
                    st.info(quiz.get("dialogue_amis", "無對話資料"))
                    
                with st.form(key=f"ld_form_{q_idx}"):
                    opts = quiz["options"].copy()
                    if f"ld_opts_{q_idx}" not in st.session_state:
                        random.shuffle(opts)
                        st.session_state[f"ld_opts_{q_idx}"] = opts
                        
                    choice = st.radio("選項：", st.session_state[f"ld_opts_{q_idx}"], index=None)
                    if st.form_submit_button("📥 提交答案"):
                        if choice == quiz["correct_text"]:
                            st.success(f"✓ 正確：{quiz['correct_text']}")
                        else:
                            st.error(f"✕ 錯誤，正確應為：{quiz['correct_text']}")
                            
                if mode == "隨機挑題" and st.button("➡️ 下一題", key=f"ld_next_{q_idx}"):
                    st.session_state.ld_ptr += 1
                    st.rerun()
            else:
                st.success("🎉 本輪隨機題組已完成！")
                if st.button("🔄 重新挑戰"):
                    st.session_state.ld_ptr = 0
                    random.shuffle(st.session_state.ld_order)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif current_tab == "🗣️ 口說":
    st.subheader("🗣️ 口說測驗 (pisowal)")
    st.divider()
    sub_tab = st.radio("題型選擇：", ["段落朗讀", "情境問答", "看圖表達"], horizontal=True)
    
    if sub_tab == "段落朗讀":
        if not DB_SPEAKING_READ:
            st.warning("📭 段落朗讀題庫建置中")
        else:
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            opts = {f"題目 {q['quiz_id']}: {q['title']}": q for q in DB_SPEAKING_READ}
            sel = st.selectbox("請選擇朗讀題目：", list(opts.keys()))
            if sel:
                q = opts[sel]
                font_size = st.slider("🔍 字體大小", 16, 48, 24, 2)
                st.markdown(f"<div style='padding:20px; border-radius:10px; background:rgba(13,148,136,0.1); border-left:5px solid #0D9488; font-size:{font_size}px;'>{q['content']}</div>", unsafe_allow_html=True)
                st.caption(f"來源：{q.get('source', '無')} ｜ 建議時間：1.5分鐘")
            st.markdown('</div>', unsafe_allow_html=True)
            
    elif sub_tab == "情境問答":
        if not DB_SPEAKING_QA:
            st.warning("📭 情境問答題庫建置中")
        else:
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            mode = st.radio("模式：", ["隨機挑題", "自主選題"], horizontal=True)
            
            # 🛡️ 狀態解耦防禦
            if "sqa_ptr" not in st.session_state:
                st.session_state.sqa_ptr = 0
            if "sqa_order" not in st.session_state or len(st.session_state.sqa_order) != len(DB_SPEAKING_QA):
                st.session_state.sqa_order = list(range(len(DB_SPEAKING_QA)))
                random.shuffle(st.session_state.sqa_order)
                
            q_idx = st.session_state.sqa_order[st.session_state.sqa_ptr] if mode == "隨機挑題" else st.selectbox("選定題組：", range(len(DB_SPEAKING_QA)), format_func=lambda x: f"第 {x+1} 題")
            
            if st.session_state.sqa_ptr < len(DB_SPEAKING_QA) or mode == "自主選題":
                q = DB_SPEAKING_QA[q_idx]
                audio_path = f"assets/audio/02_speaking/speaking_qa/situation_{str(q.get('quiz_id', q_idx)).zfill(2)}.mp3"
                if os.path.exists(audio_path):
                    st.audio(audio_path, format="audio/mp3")
                else:
                    st.info("💡 音檔製作中")
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.toggle("👁️ 顯示族語", key=f"sqa_amis_{q_idx}"):
                        st.info(f"💬 {q.get('question_amis', '')}")
                with c2:
                    if st.toggle("👁️ 顯示中文", key=f"sqa_ch_{q_idx}"):
                        st.markdown(f"> 💡 {q.get('question_ch', '')}")
                        
                with st.expander("📥 顯示參考答案"):
                    st.success(f"✨ **族語:**\n{q.get('suggested_answer_amis', '')}\n\n💡 **中文:**\n{q.get('suggested_answer_ch', '')}")
                
                if mode == "隨機挑題" and st.button("➡️ 下一題", key=f"sqa_next_{q_idx}"):
                    st.session_state.sqa_ptr += 1
                    st.rerun()
            else:
                st.success("🎉 情境問答隨機練習已完成！")
                if st.button("🔄 重新挑戰"):
                    st.session_state.sqa_ptr = 0
                    random.shuffle(st.session_state.sqa_order)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
    elif sub_tab == "看圖表達":
        if not DB_SPEAKING_IMG:
            st.warning("📭 看圖表達題庫建置中")
        else:
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            opts = {q["title"]: q for q in DB_SPEAKING_IMG}
            sel = st.selectbox("主題選擇：", list(opts.keys()))
            if sel:
                q = opts[sel]
                
                # 🚀 變更點：智慧路徑掛載 (Smart Path Resolver)
                raw_img_name = q.get("image_path", "")
                
                # 如果 JSON 中只有檔名 (如 "01.jpg")，系統自動補全 assets/images/ 前綴
                # 如果已經是完整路徑，則保持原狀，確保向下相容
                if not raw_img_name.startswith("assets/") and raw_img_name != "":
                    target_img_path = os.path.join("assets", "images", raw_img_name)
                else:
                    target_img_path = raw_img_name

                if os.path.exists(target_img_path):
                    st.image(target_img_path, use_container_width=True)
                else:
                    st.error(f"⚠️ 圖片遺失：系統找不到 `{target_img_path}`，請確認檔案已放置於該目錄。")
                
                if st.toggle("📝 顯示草稿區", key=f"img_draft_{q.get('quiz_id', 0)}"):
                    st.text_area("寫下回答提示：", key=f"draft_txt_{q.get('quiz_id', 0)}")
                
                with st.expander("📥 參考答案"):
                    st.success(f"**族語:** {q.get('suggested_answer_amis', '')}\n\n**中文:** {q.get('suggested_answer_ch', '')}")
            st.markdown('</div>', unsafe_allow_html=True)

elif current_tab == "📖 閱讀":
    st.subheader("📖 閱讀測驗 (piasip)")
    st.divider()
    if not DB_READING:
        st.warning("📭 閱讀題庫建置中")
    else:
        target_type = "vocabulary" if st.radio("題型：", ["選擇題-詞彙語意", "選擇題-語言結構"], horizontal=True) == "選擇題-詞彙語意" else "structure"
        db = [item for item in DB_READING if item.get("type") == target_type]
        
        if db:
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            state_ptr = f"r_{target_type}_ptr"
            state_order = f"r_{target_type}_order"
            
            # 🛡️ 狀態解耦防禦
            if state_ptr not in st.session_state:
                st.session_state[state_ptr] = 0
            
            if state_order not in st.session_state or len(st.session_state[state_order]) != len(db):
                st.session_state[state_order] = list(range(len(db)))
                random.shuffle(st.session_state[state_order])
            
            ptr = st.session_state[state_ptr]
            if ptr < len(db):
                q = db[st.session_state[state_order][ptr]]
                st.write(f"**[進度：第 {ptr + 1} 題 / 共 {len(db)} 題]**")
                st.write(q["question_text"])
                
                with st.form(key=f"r_form_{target_type}_{ptr}"):
                    opts = q["options"].copy()
                    if f"r_opts_{target_type}_{ptr}" not in st.session_state:
                        random.shuffle(opts)
                        st.session_state[f"r_opts_{target_type}_{ptr}"] = opts
                    
                    choice = st.radio("請選擇：", st.session_state[f"r_opts_{target_type}_{ptr}"], index=None)
                    if st.form_submit_button("📥 提交"):
                        meaning = q.get("chinese_meaning", "")
                        disp_ans = f"{q['correct_text']} ({meaning})" if meaning else q['correct_text']
                        if choice == q['correct_text']:
                            st.success(f"✓ 正確答案：{disp_ans}")
                        else:
                            st.error(f"✕ 錯誤，答案為：{disp_ans}")
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("⬅️ 上一題", disabled=(ptr==0), key=f"r_prev_{target_type}_{ptr}"):
                        st.session_state[state_ptr] -= 1
                        st.rerun()
                with c2:
                    if st.button("➡️ 下一題", key=f"r_next_{target_type}_{ptr}"):
                        st.session_state[state_ptr] += 1
                        st.rerun()
            else:
                # 🚀 修復：補齊閱讀測驗到底時的重置迴圈
                st.success("🎉 您已完成本項目全部題組練習！")
                if st.button("🔄 重新洗牌挑戰", key=f"r_reset_{target_type}"):
                    st.session_state[state_ptr] = 0
                    random.shuffle(st.session_state[state_order])
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)

elif current_tab == "✍️ 寫作":
    st.subheader("✍️ 寫作測驗 (pitilid)")
    st.divider()
    if not DB_WRITING:
        st.warning("📭 寫作題庫建置中")
    else:
        target_type = "dictation" if st.radio("題型：", ["句子聽寫", "問答"], horizontal=True) == "句子聽寫" else "question"
        db = [item for item in DB_WRITING if item.get("type") == target_type]
        
        if db:
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            state_ptr = f"w_{target_type}_ptr"
            if state_ptr not in st.session_state:
                st.session_state[state_ptr] = 0
            
            ptr = st.session_state[state_ptr]
            if ptr < len(db):
                q = db[ptr]
                st.write(f"**[進度：第 {ptr + 1} 題 / 共 {len(db)} 題]**")
                
                if target_type == "dictation":
                    if os.path.exists(q.get("audio_path", "")):
                        st.audio(q["audio_path"], format="audio/mp3")
                    st.text_input("完整族語句子：", key=f"w_in_{ptr}")
                    with st.expander("📥 核對答案"):
                        st.success(q.get("correct_text", ""))
                else:
                    st.markdown(f"#### ❓ {q.get('question_text', '')}")
                    if st.toggle("👁️ 中文提示", key=f"w_hint_{ptr}"):
                        st.info(q.get("chinese_translation", ""))
                    st.text_input("輸入練習：", key=f"w_in_{ptr}")
                    with st.expander("📥 參考答案"):
                        st.success(q.get("suggested_answer", ""))
                
                if st.button("➡️ 下一題", key=f"w_next_{target_type}_{ptr}"):
                    st.session_state[state_ptr] += 1
                    st.rerun()
            else:
                st.success("🎉 練習完成！")
                if st.button("🔄 重新開始", key=f"w_reset_{target_type}"):
                    st.session_state[state_ptr] = 0
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# 頁尾
st.write("---")
st.caption(f"© 2026 中高級認證 App 三一開發團隊 ｜ 系統版本：**{APP_VERSION}**")
