import streamlit as st
import json
import os

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

# ---- 10-4. 模擬獨立資料庫加載 (Integ-CRF v9.0 轉接器模式防禦) ----
# 實務佈署時會透過 json.load() 讀取 data/listening_quiz.json 檔案
# 這裡先預載您提供的 15 題完整標準數據，並做正字法與索引清洗
QUIZ_DATA = [
    {"id": 1, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-01.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) riyar", "(2) 'alo", "(3) fanaw", "(4) sa'owac"], "correct_index": 0},
    {"id": 2, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-02.mp3", "question_text": "請聽音檔，選出語音中所唸的正確詞彙：", "options": ["(1) korkor", "(2) rohayan", "(3) romakat", "(4) rotarot"], "correct_index": 2},
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

# 1. 測驗說明頁面
if current_tab == "📋 測驗說明":
    st.subheader("📋 測驗說明 (Saheci)")
    st.markdown("""
    歡迎使用**中高級認證學習 App**！本系統專為族語中高級認證測驗設計。
    """)
    st.info("📌 目前進度：系統基礎骨架建置完成，支援雙模式視覺適應。")

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
        
        # --- 狀態管理器 (Session State) 初始化 ---
        # 用來紀錄目前使用者回答到第幾題，避免重新渲染時狀態遺失
        if "current_quiz_index" not in st.session_state:
            st.session_state.current_quiz_index = 0
        if "audio_triggered" not in st.session_state:
            st.session_state.audio_triggered = False
        if "submitted" not in st.session_state:
            st.session_state.submitted = False

        idx = st.session_state.current_quiz_index
        
        # 實作「每次只出現一題」機制
        if idx < len(QUIZ_DATA):
            current_quiz = QUIZ_DATA[idx]
            
            # 顯示題號與題幹
            st.write(f"**第 {idx + 1} 題 / 共 {len(QUIZ_DATA)} 題**")
            st.write(current_quiz["question_text"])
            
            # --- 播放題目組件設計 ---
            # 點擊按鈕觸發單次播放音檔
            if st.button("🔊 播放題目", key=f"play_{idx}"):
                st.session_state.audio_triggered = True
            
            if st.session_state.audio_triggered:
                # 使用 Streamlit 原生播放組件，對齊自適應明暗模式
                st.audio(current_quiz["audio_path"], format="audio/mp3", autoplay=True)
                # 播放完畢後將開關重設，確保只觸發播放一遍
                st.session_state.audio_triggered = False
            
            st.write("---")
            
            # --- 答案選項顯示 (單選) ---
            # 若已提交，則鎖定選項禁止修改
            user_choice = st.radio(
                "請從下方選出正確答案：",
                options=current_quiz["options"],
                index=None,  # 預設不選取，防止先入為主的提示
                key=f"radio_{idx}",
                disabled=st.session_state.submitted
            )
            
            # --- 提交與判定機制 ---
            if not st.session_state.submitted:
                if st.button("📥 提交答案", key=f"submit_{idx}"):
                    if user_choice is None:
                        st.warning("⚠️ 請先選擇一個選項再行提交！")
                    else:
                        st.session_state.submitted = True
                        st.rerun()
            else:
                # 取得使用者選取的陣列索引與正確索引進行對帳
                selected_index = current_quiz["options"].index(user_choice)
                correct_idx = current_quiz["correct_index"]
                correct_answer_text = current_quiz["options"][correct_idx]
                
                # 以 "✓" 或 "✕" 表示答題結果並顯示正確答案
                if selected_index == correct_idx:
                    st.markdown(f"### 🔴 答題結果：✓")
                    st.success(f" Fangcal! 答對了！正確答案就是：**{correct_answer_text}**")
                else:
                    st.markdown(f"### 🔴 答題結果：✕")
                    st.error(f" 再接再厲！正確答案應該是：**{correct_answer_text}**")
                
                # 下一題導覽按鈕
                if st.button("➡️ 下一題", key=f"next_{idx}"):
                    st.session_state.current_quiz_index += 1
                    st.session_state.submitted = False
                    st.rerun()
        else:
            st.balloons()
            st.success("🎉 恭喜您！已完成「聽音選詞」全部 15 道題目的練習。")
            if st.button("🔄 重新挑戰"):
                st.session_state.current_quiz_index = 0
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
st.caption("© 2026 中高級認證 App 開發團隊 ｜ 雙模式 15 題全功能完整版")
