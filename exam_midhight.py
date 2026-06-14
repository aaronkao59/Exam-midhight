import streamlit as st
import random

# ---- 1. 頁面佈局設定 (Code-CRF v9.0 運行時配置) ----
st.set_page_config(
    page_title="中高級認證",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---- 2. 自動適應雙模式的 CSS 設計 (UIUX-CRF v9.0 視覺熵減) ----
st.markdown("""
    <style>
    /* 核心題目卡片式容器：只有顯式宣告的卡片才會擁有此風格 */
    .quiz-card {
        background-color: var(--secondary-background-color);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-top: 15px;
        margin-bottom: 25px;
        transition: all 0.3s ease;
    }
    
    /* 標題與重點文字：使用亮眼且百搭的青色 */
    h1, h2, h3 {
        color: #0D9488 !important;
    }
    
    @media (prefers-color-scheme: dark) {
        h1, h2, h3 {
            color: #2DD4BF !important;
        }
    }
    
    .stMarkdown p {
        color: var(--text-color);
        opacity: 0.85;
    }
    
    /* 覆寫提示區塊與非必要組件的預設外框，強制清除視覺干擾 */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }
    
    /* 清除 segmented_control 和 radio 可能觸發的隱性原生區塊背景 */
    div[data-testid="stHorizontalBlock"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---- App 頂部導覽列 ----
st.title("🎓 中高級認證")
st.caption("[認證考試注意事項]&[測驗平台選擇]")

# ---- 第一層：五個主要選項 (導覽選單) ----
main_options = ["📋 測驗說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
current_tab = st.segmented_control(
    "主選單導覽", 
    main_options, 
    default="📋 測驗說明",
    label_visibility="collapsed"
)

# ---- 🧠 跨頁面狀態解耦防腐層 ----
if "previous_tab" not in st.session_state:
    st.session_state.previous_tab = "📋 測驗說明"

if st.session_state.previous_tab != current_tab:
    st.session_state.submitted = False
    st.session_state.audio_triggered = False
    st.session_state.previous_tab = current_tab
    st.rerun()

# ---- 3. 原始靜態題庫 (15題標準數據庫，對齊 10-5 阿美語純詞彙與字串對帳規範) ----
QUIZ_DATA = [
    {"id": 1, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-01.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["riyar", "'alo", "fanaw", "sa'owac"], "correct_text": "riyar"},
    {"id": 2, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-02.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["korkor", "rohayan", "romakat", "rotarot"], "correct_text": "romakat"},
    {"id": 3, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-03.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["hadhad", "hakhak", "hawan", "hafay"], "correct_text": "hafay"},
    {"id": 4, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-04.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["tefo'", "'okoy", "tafokod", "tafolod"], "correct_text": "tafokod"},
    {"id": 5, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-05.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["fakar", "tayhi", "pitaw", "tarakar"], "correct_text": "pitaw"},
    {"id": 6, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-06.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["sariri'", "riri'", "siri", "riyar"], "correct_text": "siri"},
    {"id": 7, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-07.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["koleto", "lokot", "kewaw", "kakorot"], "correct_text": "koleto"},
    {"id": 8, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-08.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["siwoy", "kodasing", "konga", "damay"], "correct_text": "konga"},
    {"id": 9, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-09.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["mali'", "tikami", "tilifi", "pawli"], "correct_text": "tilifi"},
    {"id": 10, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-10.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["picakay", "pitangtang", "picaliw", "pafeli'"], "correct_text": "picakay"},
    {"id": 11, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-11.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["'olaw", "'alo", "fao", "tao"], "correct_text": "tao"},
    {"id": 12, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-12.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["rorang", "kolong", "lotong", "ekong"], "correct_text": "lotong"},
    {"id": 13, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-13.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["Halitamako", "Haliradiw", "Haliepah", "Hali'ecaw"], "correct_text": "Haliepah"},
    {"id": 14, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-14.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["dafak", "a'ayad", "dadaya", "kamaya"], "correct_text": "dadaya"},
    {"id": 15, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-15.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["sioy", "simal", "sinafel", "simico"], "correct_text": "sinafel"}
]

# ---- 第二層：根據選擇顯示對應架構 ----

# 1. 測驗說明頁面 (已完全替換為最新認證指南官方文字)
if current_tab == "📋 測驗說明":
    st.subheader("📋 測驗說明 (Saheci)")
    
    st.markdown("### 1. 詞彙範圍與參考教材")
    st.markdown("""
    * **詞彙範圍：** 學習詞表1至800詞，以及其衍生詞 。
    * **參考教材：** 包含（第1階至第9階）教材、生活會話篇、閱讀書寫篇 。
    """)
    
    st.markdown("### 2. 測驗架構與題型配分")
    st.markdown("""
    中高級認證總分為100分，由聽力（20分）、口說（30分）、閱讀（30分）與寫作（20分）四個項目組成 ：

    * **〖聽力測驗〗（20%）**
      * 聽音選詞（5題，10%）：聽族語句子，從4個詞彙或詞組選項中，選出答案 。
      * 對話理解（5題，10%）：根據2位族人的對話，從4個選項中選出答案 。
    * **〖口說測驗〗（30%）**
      * 段落朗讀（1題，10%）：朗讀約40至50詞的短文（備答1分半鐘，作答1分半鐘） 。
      * 情境問答（5題，10%）：每一題包含2句（第1句為情境鋪陳），聽完後須以完整句子表達個人看法（每題含備答時間約40秒） 。
      * 看圖表達（1題，10%）：依圖片情境以族語表達想法（備答2分鐘，作答2分鐘） 。
    * **〖閱讀測驗〗（30%）**
      * 詞彙語意（5題，10%）：依提示於4個選項中選出最符合語意的答案 。
      * 語言結構（10題，20%）：依提示於4個選項中選出最符合語法結構的答案 。
    * **〖寫作測驗〗（20%）**
      * 句子聽寫（5題，10%）：聽寫族語句子，每題播放2遍 。
      * 問答題（5題，10%）：依題目指示，以完整的族語句子作答 。
    """)
    
    st.markdown("### 3. 合格標準總結")
    st.markdown("""
    滿分100分中，**總分達60分以上**，且單項成績達**聽力15分、口說15分、閱讀18分、寫作12分以上**，即可取得「通過聽說讀寫」的完整資格 。考生亦可依對應門檻獨立取得「通過聽說」或「通過讀寫」的資格 。
    """)

# 2. 聽力測驗
elif current_tab == "🎧 聽力":
    st.subheader("🎧 聽力測驗 (Pitengilan)")
    
    listening_sub = st.radio(
        "聽力題型選擇：",
        ["選擇題-聽音選詞", "選擇題-對話理解"],
        horizontal=True
    )
    
    if listening_sub == "選擇題-聽音選詞":
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 選擇題 - 聽音選詞")
        
        # --- 🧠 雙隨機防禦快取初始化迴路 ---
        if "random_quiz_order" not in st.session_state:
            st.session_state.random_quiz_order = list(range(len(QUIZ_DATA)))
            random.shuffle(st.session_state.random_quiz_order)
            
        if "current_pointer" not in st.session_state:
            st.session_state.current_pointer = 0
        if "audio_triggered" not in st.session_state:
            st.session_state.audio_triggered = False
        if "submitted" not in st.session_state:
            st.session_state.submitted = False
        if "shuffled_options_map" not in st.session_state:
            st.session_state.shuffled_options_map = {}

        ptr = st.session_state.current_pointer
        
        if ptr < len(QUIZ_DATA):
            true_quiz_id = st.session_state.random_quiz_order[ptr]
            current_quiz = QUIZ_DATA[true_quiz_id]
            
            if true_quiz_id not in st.session_state.shuffled_options_map:
                shuffled_raw_opts = current_quiz["options"].copy()
                random.shuffle(shuffled_raw_opts)
                
                formatted_opts = []
                correct_text_formatted = ""
                correct_word_raw = current_quiz["correct_text"]
                
                for i, word_item in enumerate(shuffled_raw_opts):
                    display_text = f"({i+1}) {word_item}"
                    formatted_opts.append(display_text)
                    if word_item == correct_word_raw:
                        correct_text_formatted = display_text
                
                st.session_state.shuffled_options_map[true_quiz_id] = {
                    "options": formatted_opts,
                    "correct_text": correct_text_formatted
                }
            
            live_quiz_data = st.session_state.shuffled_options_map[true_quiz_id]
            
            st.write(f"**當前進度：第 {ptr + 1} 題 / 共 {len(QUIZ_DATA)} 題 (雙重隨機防禦版)**")
            st.write(current_quiz["question_text"])
            
            if st.button("🔊 播放題目", key=f"play_{ptr}"):
                st.session_state.audio_triggered = True
            
            if st.session_state.audio_triggered:
                st.audio(current_quiz["audio_path"], format="audio/mp3", autoplay=True)
                st.session_state.audio_triggered = False
            
            st.write("---")
            
            user_choice = st.radio(
                "請從下方選出正確答案：",
                options=live_quiz_data["options"],
                index=None,
                key=f"radio_{ptr}",
                disabled=st.session_state.submitted
            )
            
            if not st.session_state.submitted:
                if st.button("📥 提交答案", key=f"submit_{ptr}"):
                    if user_choice is None:
                        st.warning("⚠️ 請先選擇一個選項再行提交！")
                    else:
                        st.session_state.submitted = True
                        st.rerun()
            else:
                correct_answer_text = live_quiz_data["correct_text"]
                
                if user_choice == correct_answer_text:
                    st.markdown(f"### 🔴 答題結果：✓")
                    st.success(f" Fangcal! 答對了！正確答案就是：**{correct_answer_text}**")
                else:
                    st.markdown(f"### 🔴 答題結果：✕")
                    st.error(f" 再接再厲！正確答案應該是：**{correct_answer_text}**")
                
                if st.button("➡️ 下一題", key=f"next_{ptr}"):
                    st.session_state.current_pointer += 1
                    st.session_state.submitted = False
                    st.rerun()
        else:
            st.balloons()
            st.success("🎉 您已完成本輪全部 15 道隨機題目！系統正在為您重新洗牌出題...")
            if st.button("🔄 開始下一輪隨機挑戰"):
                random.shuffle(st.session_state.random_quiz_order)
                st.session_state.shuffled_options_map = {}
                st.session_state.current_pointer = 0
                st.session_state.submitted = False
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif listening_sub == "選擇題-對話理解":
        st.markdown("### 💬 選擇題 - 對話理解")
        st.warning("🚧 【內容建置中】此處未來將播放部落生活情境對話，並測試長句理解能力。")

# 3. 口說測驗
elif current_tab == "🗣️ 口說":
    st.subheader("🗣️ 口說測驗 (Pisowalan)")
    
    speaking_sub = st.radio(
        "口說題型選擇：",
        ["段落朗讀", "情境問答", "看圖表達"],
        horizontal=True
    )
    
    if speaking_sub == "段落朗讀":
        st.markdown("### 📖 段落朗讀")
        st.warning("🚧 【內容建置中】")
    elif speaking_sub == "情境問答":
        st.markdown("### ❓ 情境問答")
        st.warning("🚧 【內容建置中】")
    elif speaking_sub == "看圖表達":
        st.markdown("### 🖼️ 看圖表達")
        st.warning("🚧 【內容建置中】")

# 4. 閱讀測驗
elif current_tab == "📖 閱讀":
    st.subheader("📖 閱讀測驗 (Piasipan)")
    
    reading_sub = st.radio(
        "閱讀題型選擇：",
        ["選擇題-詞彙語意", "選擇題-語言結構"],
        horizontal=True
    )
    
    if reading_sub == "選擇題-詞彙語意":
        st.markdown("### 🏷️ 選擇題 - 詞彙語意")
        st.warning("🚧 【內容建置中】")
    elif reading_sub == "選擇題-語言結構":
        st.markdown("### ⛓️ 選擇題 - 語言結構")
        st.warning("🚧 【內容建置中】")

# 5. 寫作測驗
elif current_tab == "✍️ 寫作":
    st.subheader("✍️ 寫作測驗 (Pitilidan)")
    
    writing_sub = st.radio(
        "寫作題型選擇：",
        ["句子聽寫", "問答"],
        horizontal=True
    )
    
    if writing_sub == "句子聽寫":
        st.markdown("### ✍️ 句子聽寫")
        st.warning("🚧 【內容建置中】")
    elif writing_sub == "問答":
        st.markdown("### 📝 問答")
        st.warning("🚧 【內容建置中】")

# ---- App 底部註腳 ----
st.write("---")
st.caption("© 2026 中高級認證 App 開發團隊 ｜ 雙重隨機全防禦穩定版")
