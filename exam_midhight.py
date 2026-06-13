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
    /* 卡片式容器：自動適應背景與文字顏色，並加上細緻的主題框線 */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: var(--secondary-background-color);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    /* 標題與重點文字：使用亮眼且百搭的青色（Teal） */
    h1, h2, h3 {
        color: #0D9488 !important;
    }
    
    @media (prefers-color-scheme: dark) {
        h1, h2, h3 {
            color: #2DD4BF !important;
        }
    }
    
    .stMarkdown p, .stMarkdown li {
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

# ---- 3. 第一層導覽選單更換 (改用穩定版 st.tabs，徹底消除空框框) ----
main_options = ["📋 測驗說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
tab_objects = st.tabs(main_options)

# 透過指標動態判定使用者當前正處於哪一個分頁
current_tab = "📋 測驗說明"
for i, tab in enumerate(tab_objects):
    with tab:
        if st.runtime.exists(): # 確保在 Streamlit 運行時環境下正常映射
            current_tab = main_options[i]

st.write("") # 留空行增加視覺舒適度

# ---- 4. 原始靜態題庫 (15題標準數據庫，對齊 10-5 詞彙規範) ----
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

# 1. 📋 測驗說明頁面 (已導入正式官方內容)
if current_tab == "📋 測驗說明":
    st.subheader("📋 測驗說明 (Saheci)")
    
    st.markdown("### 📘 1. 詞彙範圍與參考教材")
    st.markdown("""
    * **詞彙範圍：** 原住民族語言學習詞表 1 至 800 詞，以及其衍生詞。
    * **參考教材：** 包含 12 階教材（第 1 階至第 9 階）、原住民族語初級教材-生活會話篇，以及原住民族語中級教材-閱讀書寫篇。
    """)
    
    st.markdown("### 📊 2. 測驗架構與題型配分")
    
    # 建立高結構化表格呈現題型與比重
    st.markdown("""
    | 測驗項目 | 題型名稱 | 題數 | 配分比重 | 題型說明 |
    | :--- | :--- | :---: | :---: | :--- |
    | **🎧 聽力測驗**<br>(佔 20%) | 聽音選詞<br>對話理解 | 5 題<br>5 題 | 10%<br>10% | 聽完句子，從 4 個選項選出最相關答案。<br>根據 2 位族人對話選出最適當答案。 |
    | **🗣️ 口說測驗**<br>(佔 30%) | 段落朗讀<br>情境問答<br>看圖表達 | 1 題<br>5 題<br>1 題 | 10%<br>10% | 朗讀 40-50 詞短文 (備答1.5分/作答1.5分)。<br>聽完情境，以完整句子表達個人看法。<br>依圖片情境以族語表達想法 (備答2分/作答2分)。 |
    | **📖 閱讀測驗**<br>(佔 30%) | 詞彙語意<br>語言結構 | 5 題<br>10 題 | 10%<br>20% | 依提示於 4 個選項中選出符合語意的答案。<br>依提示於 4 個選項中選出符合語法結構的答案。 |
    | **✍️ 寫作測驗**<br>(佔 20%) | 句子聽寫<br>問答題 | 5 題<br>5 題 | 10%<br>10% | 聽寫族語句子，每題播放 2 遍。<br>依題目指示，以完整的族語句子作答。 |
    """)
    
    st.markdown("### 🏆 3. 合格標準總結")
    st.success("""
    **🎯 完整合格門檻（滿分 100 分，達 60 分以上通過）：**
    * 總分達 **60 分** 以上。
    * 且各單項成績必須同時達到最低門檻：
        * **聽力：** 15 分 以上 (滿分 20)
        * **口說：** 15 分 以上 (滿分 30)
        * **閱讀：** 18 分 以上 (滿分 30)
        * **寫作：** 12 分 以上 (滿分 20)
    
    *💡 備註：考生亦可依對應門檻獨立取得「通過聽說」或「通過讀寫」的合格資格。*
    """)

# 2. 🎧 聽力模組 (雙隨機核心防護版)
elif current_tab == "🎧 聽力":
    st.subheader("🎧 聽力模組 (Pitengilan)")
    st.write("請選擇下方的題型開始練習：")
    
    listening_sub = st.radio(
        "聽力題型選擇：",
        ["選擇題-聽音選詞", "選擇題-對話理解"],
        horizontal=True
    )
    
    if listening_sub == "選擇題-聽音選詞":
        st.markdown("### 🔍 選擇題 - 聽音選詞 (5題，佔10%)")
        
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
                shuffled_opts = current_quiz["options"].copy()
                random.shuffle(shuffled_opts)
                original_correct_text = current_quiz["options"][current_quiz["correct_index"]]
                new_correct_index = shuffled_opts.index(original_correct_text)
                st.session_state.shuffled_options_map[true_quiz_id] = {
                    "options": shuffled_opts,
                    "correct_index": new_correct_index
                }
            
            live_quiz_data = st.session_state.shuffled_options_map[true_quiz_id]
            
            st.write(f"**當前進度：第 {ptr + 1} 題 / 共 {len(QUIZ_DATA)} 題**")
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
                selected_index = live_quiz_data["options"].index(user_choice)
                correct_idx = live_quiz_data["correct_index"]
                correct_answer_text = live_quiz_data["options"][correct_idx]
                
                if selected_index == correct_idx:
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
            st.success("🎉 您已完成本輪全部 15 道隨機練習題目！")
            if st.button("🔄 開始下一輪隨機挑戰"):
                random.shuffle(st.session_state.random_quiz_order)
                st.session_state.shuffled_options_map = {}
                st.session_state.current_pointer = 0
                st.session_state.submitted = False
                st.rerun()
        
    elif listening_sub == "選擇題-對話理解":
        st.markdown("### 💬 選擇題 - 對話理解 (5題，佔10%)")
        st.warning("🚧 【內容建置中】預計依據雙人生活對話文本，加載 4 選 1 字串判讀組件。")

# 3. 🗣️ 口說模組
elif current_tab == "🗣️ 口說":
    st.subheader("🗣️ 口說模組 (Pisowalan)")
    st.write("請選擇下方的題型開始練習：")
    
    speaking_sub = st.radio(
        "口說題型選擇：",
        ["段落朗讀", "情境問答", "看圖表達"],
        horizontal=True
    )
    
    if speaking_sub == "段落朗讀":
        st.markdown("### 📖 段落朗讀 (1題，佔10%)")
        st.warning("🚧 【內容建置中】預計導入 40-50 詞短文，並提供 1 分半鐘倒數計時器。")
    elif speaking_sub == "情境問答":
        st.markdown("### ❓ 情境問答 (5題，佔10%)")
        st.warning("🚧 【內容建置中】預計導入雙句情境音檔，並開通 40 秒完整句答題錄音。")
    elif speaking_sub == "看圖表達":
        st.markdown("### 🖼️ 看圖表達 (1題，佔10%)")
        st.warning("🚧 【內容建置中】預計導入文化插圖格柵，並開啟 2 分鐘多巴胺成癮式口說練習。")

# 4. 📖 閱讀模組
elif current_tab == "📖 閱讀":
    st.subheader("📖 閱讀模組 (Piasipan)")
    st.write("請選擇下方的題型開始練習：")
    
    reading_sub = st.radio(
        "閱讀題型選擇：",
        ["選擇題-詞彙語意", "選擇題-語言結構"],
        horizontal=True
    )
    
    if reading_sub == "選擇題-詞彙語意":
        st.markdown("### 🏷️ 選擇題 - 詞彙語意 (5題，佔10%)")
        st.warning("🚧 【內容建置中】預計對接 1-800 詞表之衍生詞語意矩陣。")
    elif reading_sub == "選擇題-語言結構":
        st.markdown("### ⛓️ 選擇題 - 語言結構 (10題，佔20%)")
        st.warning("🚧 【內容建置中】預計針對 VSO 結構、主事/受事焦點系統進行題庫擴充。")

# 5. ✍️ 寫作模組
elif current_tab == "✍️ 寫作":
    st.subheader("✍️ 寫作模組 (Pitilidan)")
    st.write("請選擇下方的題型開始練習：")
    
    writing_sub = st.radio(
        "寫作題型選擇：",
        ["句子聽寫", "問答"],
        horizontal=True
    )
    
    if writing_sub == "句子聽寫":
        st.markdown("### ✍️ 句子聽寫 (5題，佔10%)")
        st.warning("🚧 【內容建置中】預計導入每題播放 2 遍之正字法符號鍵盤輸入器。")
    elif writing_sub == "問答":
        st.markdown("### 📝 問答題 (5題，佔10%)")
        st.warning("🚧 【內容建置中】預計導入完整族語長句書面論述區塊。")

# ---- App 底部註腳 ----
st.write("---")
st.caption("© 2026 中高級認證 App 開發團隊 ｜ 雙模式官方簡章同步版")
