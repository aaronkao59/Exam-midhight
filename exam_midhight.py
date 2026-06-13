import streamlit as st
import random

# ---- 10-1. 頁面佈局設定 (Code-CRF v9.0 運行時配置) ----
st.set_page_config(
    page_title="中高級認證",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---- 10-3. 自動適應雙模式的 CSS 設計 (UIUX-CRF v9.0 視覺熵減) ----
st.markdown("""
    <style>
    /* 卡片式容器：自動適應背景與文字顏色 */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: var(--secondary-background-color);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
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
    
    .stAlert {
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)
st.caption("族語認證數位學習平台")

# ---- App 頂部導覽列 ----
st.title("🎓 中高級認證")

# ---- 第一層：五個主要選項 (導覽選單) ----
main_options = ["📋 測驗說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
current_tab = st.segmented_control(
    "主選單導覽", 
    main_options, 
    default="📋 測驗說明",
    label_visibility="collapsed"
)

st.write("") 

# ---- 10-4. 原始靜態題庫 (15題標準數據庫，對齊 10-5 詞彙規範) ----
QUIZ_DATA = [
    {"id": 1, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-01.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) riyar", "(2) 'alo", "(3) fanaw", "(4) sa'owac"], "correct_index": 0},
    {"id": 2, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-02.mp3", "question_text": "請聽音檔 =選出語音中所唸的正確詞彙：", "options": ["(1) korkor", "(2) rohayan", "(3) romakat", "(4) rotarot"], "correct_index": 2},
    {"id": 3, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-03.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) hadhad", "(2) hakhak", "(3) hawan", "(4) hafay"], "correct_index": 3},
    {"id": 4, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-04.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) tefo'", "(2) 'okoy", "(3) tafokod", "(4) tafolod"], "correct_index": 2},
    {"id": 5, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-05.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) fakar", "(2) tayhi", "(3) pitaw", "(4) tarakar"], "correct_index": 2},
    {"id": 6, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-06.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) sariri'", "(2) riri'", "(3) siri", "(4) riyar"], "correct_index": 2},
    {"id": 7, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-07.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) koleto", "(2) lokot", "(3) kewaw", "(4) kakorot"], "correct_index": 0},
    {"id": 8, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-08.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) siwoy", "(2) kodasing", "(3) konga", "(4) damay"], "correct_index": 2},
    {"id": 9, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-09.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) mali'", "(2) tikami", "(3) tilifi", "(4) pawli"], "correct_index": 2},
    {"id": 10, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-10.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) picakay", "(2) pitangtang", "(3) picaliw", "(4) pafeli'"], "correct_index": 0},
    {"id": 11, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-11.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) 'olaw", "(2) 'alo", "(3) fao", "(4) tao"], "correct_index": 3},
    {"id": 12, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-12.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) rorang", "(2) kolong", "(3) lotong", "(4) ekong"], "correct_index": 2},
    {"id": 13, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-13.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) Halitamako", "(2) Haliradiw", "(3) Haliepah", "(4) Hali'ecaw"], "correct_index": 2},
    {"id": 14, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-14.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) dafak", "(2) a'ayad", "(3) dadaya", "(4) kamaya"], "correct_index": 2},
    {"id": 15, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-15.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) sioy", "(2) simal", "(3) sinafel", "(4) simico"], "correct_index": 2}
]

# ---- 第二層：根據選擇顯示對應架構 ----

if current_tab == "📋 測驗說明":
    st.subheader("📋 測驗說明 (Saheci)")
    st.markdown("""
    歡迎使用**中高級認證學習 App**！本系統專為族語中高級認證測驗設計。
    """)
    st.info("📌 目前進度：支援題目雙重隨機防禦（題目順序隨機 + 選項順序隨機）。")

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
        
        # --- 🧠 雙重隨機核心初始化迴路 ---
        # 1. 鎖定題目隨機順序
        if "random_quiz_order" not in st.session_state:
            st.session_state.random_quiz_order = list(range(len(QUIZ_DATA)))
            random.shuffle(st.session_state.random_quiz_order)
            
        if "current_pointer" not in st.session_state:
            st.session_state.current_pointer = 0
        if "audio_triggered" not in st.session_state:
            st.session_state.audio_triggered = False
        if "submitted" not in st.session_state:
            st.session_state.submitted = False

        # 2. 🚀 [本期亮眼特點] 鎖定當前題目的「隨機選項順序」
        # 為避免網頁更新導致選項亂跳，我們在 Session State 中對每一題進行局部環境隔離
        if "shuffled_options_map" not in st.session_state:
            st.session_state.shuffled_options_map = {}

        ptr = st.session_state.current_pointer
        
        if ptr < len(QUIZ_DATA):
            true_quiz_id = st.session_state.random_quiz_order[ptr]
            current_quiz = QUIZ_DATA[true_quiz_id]
            
            # 檢查這一題是否已經生成過隨機選項順序，若無則立刻原地洗牌
            if true_quiz_id not in st.session_state.shuffled_options_map:
                shuffled_opts = current_quiz["options"].copy()
                random.shuffle(shuffled_opts)
                
                # 重新計算正確答案在洗牌後的新索引位置
                original_correct_text = current_quiz["options"][current_quiz["correct_index"]]
                new_correct_index = shuffled_opts.index(original_correct_text)
                
                # 將洗牌後的正確配對數據寫入快取鎖，實現反脆弱防護
                st.session_state.shuffled_options_map[true_quiz_id] = {
                    "options": shuffled_opts,
                    "correct_index": new_correct_index
                }
            
            # 從快取鎖讀取這題專屬的隨機選項與索引
            live_quiz_data = st.session_state.shuffled_options_map[true_quiz_id]
            
            st.write(f"**當前進度：第 {ptr + 1} 題 / 共 {len(QUIZ_DATA)} 題 (雙重隨機模式)**")
            st.write(current_quiz["question_text"])
            
            # --- 播放題目按鈕 ---
            if st.button("🔊 播放題目", key=f"play_{ptr}"):
                st.session_state.audio_triggered = True
            
            if st.session_state.audio_triggered:
                st.audio(current_quiz["audio_path"], format="audio/mp3", autoplay=True)
                st.session_state.audio_triggered = False
            
            st.write("---")
            
            # --- 答案選項顯示 (使用已洗牌的選項) ---
            user_choice = st.radio(
                "請從下方選出正確答案：",
                options=live_quiz_data["options"],
                index=None,  # 預設不選取
                key=f"radio_{ptr}",
                disabled=st.session_state.submitted
            )
            
            # --- 提交與判定機制 ---
            if not st.session_state.submitted:
                if st.button("📥 提交答案", key=f"submit_{ptr}"):
                    if user_choice is None:
                        st.warning("⚠️ 請先選擇一個選項再行提交！")
                    else:
                        st.session_state.submitted = True
                        st.rerun()
            else:
                # 拿當前的單選索引，與快取鎖中的 live_quiz_data["correct_index"] 進行精準對帳
                selected_index = live_quiz_data["options"].index(user_choice)
                correct_idx = live_quiz_data["correct_index"]
                correct_answer_text = live_quiz_data["options"][correct_idx]
                
                if selected_index == correct_idx:
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
            st.balloons()
            st.success("🎉 您已完成本輪全部 15 道雙重隨機題目！系統正在為您重新洗牌出題...")
            
            if st.button("🔄 開始下一輪隨機挑戰"):
                # 清空題號與選項快取，全面重新洗牌，開啟下一輪閉環
                random.shuffle(st.session_state.random_quiz_order)
                st.session_state.shuffled_options_map = {}
                st.session_state.current_pointer = 0
                st.session_state.submitted = False
                st.rerun()
        
    elif listening_sub == "選擇題-對話理解":
        st.markdown("### 💬 選擇題 - 對話理解")
        st.warning("🚧 【內容建置中】")

else:
    st.warning("🚧 【內容建置中】")

# ---- App 底部註腳 ----
st.write("---")
st.caption("© 2026 中高級認證 App 開發團隊 ｜ 題目+選項雙隨機安全版")
