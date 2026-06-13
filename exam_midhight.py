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
    /* 卡片式容器：自動適應背景與文字顏色，加上細緻的主題框線 */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: var(--secondary-background-color);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    /* 標題與重點文字：使用亮眼且百搭的青色，明暗模式下皆具備優異閱讀性 */
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
    
    .stAlert {
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---- App 頂部導覽列 ----
st.title("🎓 中高級認證")
st.caption("族語認證數位學習平台")

# ---- 第一層：五個主要選項 (導覽選單) ----
main_options = ["📋 測驗說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
current_tab = st.segmented_control(
    "主選單導覽", 
    main_options, 
    default="📋 測驗說明",
    label_visibility="collapsed"
)

st.write("") 

# ---- 🧠 [核心防護補丁] 跨頁面狀態解耦防腐層 ----
if "previous_tab" not in st.session_state:
    st.session_state.previous_tab = "📋 測驗說明"

# 當偵測到使用者切換了最上方的五個大頁籤時，無情清空過往的局部點擊狀態，阻斷跨分頁記憶體污染
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

# 1. 測驗說明頁面
if current_tab == "📋 測驗說明":
    st.subheader("📋 測驗說明 (Saheci)")
    st.markdown("歡迎使用**中高級認證學習 App**！本系統專為族語中高級認證測驗設計。")
    st.info("📌 目前進度：雙隨機安全快取鎖升級，已排除 NameError 語法異常。")

# 2. 聽力模組
elif current_tab == "🎧 聽力":
    st.subheader("🎧 聽力模組 (Pitengilan)")
    st.write("請選擇下方的題型開始練習：")
    
    listening_sub = st.radio(
        "聽力題型選擇：",
        ["選擇題-聽音選詞", "選擇題-對話理解"],
        horizontal=True
    )
    
    if listening_sub == "選擇題-聽音選詞":
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
        
        # 判斷一輪（15 題）是否全部作答完畢
        if ptr < len(QUIZ_DATA):
            true_quiz_id = st.session_state.random_quiz_order[ptr]
            current_quiz = QUIZ_DATA[true_quiz_id]
            
            # 🛡️ 核心修復補丁：使用高內聚低耦合的查表架構，徹底抹除未定義變數漏洞
            if true_quiz_id not in st.session_state.shuffled_options_map:
                shuffled_raw_opts = current_quiz["options"].copy()
                random.shuffle(shuffled_raw_opts) # 隨機打亂四個選項順序
                
                # 建立新一輪帶有編號的動態格式化清單
                formatted_opts = []
                correct_text_formatted = ""
                correct_word_raw = current_quiz["correct_text"]
                
                for i, word_item in enumerate(shuffled_raw_opts):
                    display_text = f"({i+1}) {word_item}"
                    formatted_opts.append(display_text)
                    # 精準鎖定正確字串的渲染結果
                    if word_item == correct_word_raw:
                        correct_text_formatted = display_text
                
                # 物理防護層：鎖定快取狀態
                st.session_state.shuffled_options_map[true_quiz_id] = {
                    "options": formatted_opts,
                    "correct_text": correct_text_formatted
                }
            
            # 從防護鎖中取出穩定的隨機選項數據
            live_quiz_data = st.session_state.shuffled_options_map[true_quiz_id]
            
            st.write(f"**當前進度：第 {ptr + 1} 題 / 共 {len(QUIZ_DATA)} 題 (雙重隨機防禦版)**")
            st.write(current_quiz["question_text"])
            
            # --- 播放題目按鈕 ---
            if st.button("🔊 播放題目", key=f"play_{ptr}"):
                st.session_state.audio_triggered = True
            
            if st.session_state.audio_triggered:
                st.audio(current_quiz["audio_path"], format="audio/mp3", autoplay=True)
                st.session_state.audio_triggered = False
            
            st.write("---")
            
            # --- 答案選項顯示 (單選，綁定快取後的隨機編號清單) ---
            user_choice = st.radio(
                "請從下方選出正確答案：",
                options=live_quiz_data["options"],
                index=None, # 預設不選取，避免誘導
                key=f"radio_{ptr}",
                disabled=st.session_state.submitted
            )
            
            # --- 提交與 「✓」/「✕」 判定機制 ---
            if not st.session_state.submitted:
                if st.button("📥 提交答案", key=f"submit_{ptr}"):
                    if user_choice is None:
                        st.warning("⚠️ 請先選擇一個選項再行提交！")
                    else:
                        st.session_state.submitted = True
                        st.rerun()
            else:
                # 字串安全對帳：直接拿點選文字跟快取中的正確答案字串比對，100% 關閉 ValueError 漏洞
                correct_answer_text = live_quiz_data["correct_text"]
                
                if user_choice == correct_answer_text:
                    st.markdown(f"### 🔴 答題結果：✓")
                    st.success(f" Fangcal! 答對了！正確答案就是：**{correct_answer_text}**")
                else:
                    st.markdown(f"### 🔴 答題結果：✕")
                    st.error(f" 再接再厲！正確答案應該是：**{correct_answer_text}**")
                
                # 下一題導覽
                if st.button("➡️ 下一題", key=f"next_{ptr}"):
                    st.session_state.current_pointer += 1
                    st.session_state.submitted = False
                    st.rerun()
        else:
            # 觸發均值回歸與重新洗牌：15 題全部輪完後，清除舊快取，全面重新隨機洗牌，且不重複出現
            st.balloons()
            st.success("🎉 您已完成本輪全部 15 道隨機題目！系統正在為您重新洗牌出題...")
            if st.button("🔄 開始下一輪隨機挑戰"):
                random.shuffle(st.session_state.random_quiz_order) # 重新排序題序
                st.session_state.shuffled_options_map = {}         # 清空並重置選項洗牌鎖
                st.session_state.current_pointer = 0                # 指針歸零
                st.session_state.submitted = False
                st.rerun()
        
    elif listening_sub == "選擇題-對話理解":
        st.markdown("### 💬 選擇題 - 對話理解")
        st.warning("🚧 【內容建置中】此處未來將播放部落生活情境對話，並測試長句理解能力。")

# 3. 口說模組
elif current_tab == "🗣️ 口說":
    st.subheader("🗣️ 口說模組 (Pisowalan)")
    st.write("請選擇下方的題型開始練習：")
    
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

# 4. 閱讀模組
elif current_tab == "📖 閱讀":
    st.subheader("📖 閱讀模組 (Piasipan)")
    st.write("請選擇下方的題型開始練習：")
    
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

# 5. 寫作模組
elif current_tab == "✍️ 寫作":
    st.subheader("✍️ 寫作模組 (Pitilidan)")
    st.write("請選擇下方的題型開始練習：")
    
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
