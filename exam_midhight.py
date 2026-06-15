import streamlit as st
import random
import json
import os  # 引入 OS 模組，用於物理檔案路徑防禦性偵測

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
    
    /* 小字性質註記樣式 */
    .category-note {
        font-size: 13px !important;
        color: gray !important;
        margin-top: -10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ---- App 頂部導覽列 ----
st.title("🎓 中高級認證")
st.caption("[練習平台選擇器]")

# ---- 第一層：五個主要選項 (導覽選單) ----
main_options = ["📋 認證考試說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
current_tab = st.segmented_control(
    "主選單導覽", 
    main_options, 
    default="📋 認證考試說明",
    label_visibility="collapsed"
)

# ---- 🧠 跨頁面狀態解耦防腐層 ----
if "previous_tab" not in st.session_state:
    st.session_state.previous_tab = "📋 認證考試說明"

if st.session_state.previous_tab != current_tab:
    st.session_state.submitted = False
    st.session_state.audio_triggered = False
    if "writing_submitted" in st.session_state:
        st.session_state.writing_submitted = False
    
    # 🛡️ 鋼鐵防禦：使用 del 安全註銷屬性，徹底根除問答題切換分頁時的 AttributeError 閃退死結
    if "q_show_trans" in st.session_state:
        del st.session_state["q_show_trans"]
    if "q_show_ans" in st.session_state:
        del st.session_state["q_show_ans"]
    if "s_show_q_trans" in st.session_state:
        del st.session_state["s_show_q_trans"]
    if "s_show_ans" in st.session_state:
        del st.session_state["s_show_ans"]
        
    st.session_state.previous_tab = current_tab
    st.rerun()

# ---- 3. 原始聽力題庫 (15題標準數據庫) ----
QUIZ_DATA = [
    {"id": 1, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-01.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["riyar", "'alo", "fanaw", "sa'owac"], "correct_text": "riyar"},
    {"id": 2, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-02.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["korkor", "rohayan", "romakat", "rotarot"], "correct_text": "romakat"},
    {"id": 3, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-03.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["hadhad", "hakhak", "hawan", "hafay"], "correct_text": "hafay"},
    {"id": 4, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-04.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["tefo'", "'okoy", "tafokod", "tafolod"], "correct_text": "tafokod"},
    {"id": 5, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-05.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["fakar", "tayhi", "pitaw", "tarakar"], "correct_text": "pitaw"},
    {"id": 6, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-06.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["sariri'", "riri'", "siri", "riyar"], "correct_text": "siri"},
    {"id": 7, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-07.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["koleto", "lokot", "kewaw", "kakorot"], "correct_text": "koleto"},
    {"id": 8, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-08.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["siwoy", "kodasing", "konga", "damay"], "correct_text": "konga"},
    {"id": 9, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-09.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["mali'", "tikami", "tilifi", "pawli"], "correct_text": "tilifi"},
    {"id": 10, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-10.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["picakay", "pitangtang", "picaliw", "pafeli'"], "correct_text": "picakay"},
    {"id": 11, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-11.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["'olaw", "'alo", "fao", "tao"], "correct_text": "tao"},
    {"id": 12, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-12.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["rorang", "kolong", "lotong", "ekong"], "correct_text": "lotong"},
    {"id": 13, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-13.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["Halitamako", "Haliradiw", "Haliepah", "Hali'ecaw"], "correct_text": "Haliepah"},
    {"id": 14, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-14.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["dafak", "a'ayad", "dadaya", "kamaya"], "correct_text": "dadaya"},
    {"id": 15, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-15.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["sioy", "simal", "sinafel", "simico"], "correct_text": "sinafel"}
]

# ---- 第二層：根據選擇顯示對應架構 ----

# 1. 📋 認證考試說明頁面
if current_tab == "📋 認證考試說明":
    st.subheader("📋 認證考試說明")
    st.divider()
    st.markdown("### 1. 詞彙範圍/參考教材")
    st.markdown("""
    * **詞彙範圍：** 學習詞表1至800詞，以及其衍生詞。
    * **參考教材：** 包含（第1階至第9階）教材、生活會話篇、閱讀書寫篇。
    """)
    st.markdown("### 2. 測驗架構/題型配分")
    st.markdown("""
    中高級認證總分為100分，[聽力(20分)/口說(30分)/閱讀(30分)/寫作(20分)四個項目]
    * **〖聽力測驗〗**
      * 聽音選詞(5題/10%)：聽族語句子，從4個詞彙或詞組選項中，選出答案。
      * 對話理解(5題/10%)：根據2位族人的對話，從4個選項中選出答案。
    * **〖口說測驗〗**
      * 段落朗讀(1題/10%)：朗讀40至50詞的短文(備答1分半鐘，作答1分半鐘)。
      * 情境問答(5題/10%)：每題包含2句(第1句為情境鋪陳)，以族語表達看法(每題含備答時間約40秒)。
      * 看圖表達(1題/10%)：依圖片情境以族語表達想法（備答2分鐘，作答2分鐘)。
    * **〖閱讀測驗〗**
      * 詞彙語意(5題/10%)：依提示於4個選項中選出答案。
      * 語言結構(10題/20%)：依提示於4個選項中選出答案。
    * **〖寫作測驗〗**
      * 句子聽寫(5題/10%)：聽寫族語句子，每題播放2遍。
      * 問答題(5題/10%)：依題目指示，以族語句子回答。
    """)
    st.markdown("### 3. 合格標準")
    st.markdown("""
    滿分100分中，**總分達60分以上**，且單項成績達**聽力15分、口說15分、閱讀18分、寫作12分以上**，即可取得「通過聽說讀寫」的完整資格 。考生亦可依對應門檻獨立取得「通過聽說」或「通過讀寫」的資格 。
    """)

# 2. 🎧 聽力測驗
elif current_tab == "🎧 聽力":
    st.subheader("🎧 聽力測驗 (Pitengilan)")
    st.divider()
    listening_sub = st.radio(
        "聽力題型選擇：",
        ["選擇題-聽音選詞", "選擇題-對話理解"],
        horizontal=True
    )
    
    if listening_sub == "選擇題-聽音選詞":
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 選擇題 - 聽音選詞")
        
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
            
            st.write(f"**當前進度：第 {ptr + 1} 題 / 共 {len(QUIZ_DATA)} 題**")
            st.write(current_quiz["question_text"])
            
            if st.button("🔊 播放題目", key=f"play_{ptr}"):
                st.session_state.audio_triggered = True
            
            if st.session_state.audio_triggered:
                if os.path.exists(current_quiz["audio_path"]):
                    st.audio(current_quiz["audio_path"], format="audio/mp3", autoplay=True)
                else:
                    st.warning(f"⚠️ 找不到音檔：`{current_quiz['audio_path']}`，請確認檔案是否已上傳。")
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
                    st.success(f" Fangcal! 正確答案：**{correct_answer_text}**")
                else:
                    st.markdown(f"### 🔴 答題結果：✕")
                    st.error(f" 再接再厲！正確答案：**{correct_answer_text}**")
                
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

# 3. 🗣️ 口說測驗
elif current_tab == "🗣️ 口說":
    st.subheader("🗣️ 口說測驗 (Pisowalan)")
    st.divider()
    speaking_sub = st.radio(
        "口說題型選擇：",
        ["段落朗讀", "情境問答", "看圖表達"],
        horizontal=True
    )
    
    if speaking_sub == "段落朗讀":
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown("### 📖 口說測驗 - 段落朗讀")
        
        try:
            with open("data/speaking_quiz.json", "r", encoding="utf-8") as f:
                speaking_db = json.load(f)
                
            menu_options = ["題目選單..."] + [f"題目{item['quiz_id']}：{item['title']}" for item in speaking_db]
            
            selected_quiz = st.selectbox(
                "請選擇朗讀題目：",
                options=menu_options,
                index=0,
                key="speaking_quiz_selector"
            )
            
            st.divider()
            
            if selected_quiz == "題目選單...":
                st.info("💡 點選上方選單，選擇想要挑戰的題目。")
            else:
                current_id = selected_quiz.split("：")[0].replace("題目", "")
                current_article = next((item for item in speaking_db if str(item["quiz_id"]) == str(current_id)), None)
                
                if current_article:
                    st.markdown(f"#### 🎯 {current_article['title']}")
                    st.info(current_article["content"])
                    st.caption(f"來源：{current_article['source']} ｜ 建議準備時間：1分半鐘 ｜ 建議朗讀時間：1分半鐘")
                else:
                    st.error("⚠️ 找不到該題目的對應內容，請重新選擇。")
                
        except FileNotFoundError:
            st.error("☠️ 系統性毀滅異常：偵測到 `data/speaking_quiz.json` 檔案遺失，請檢查 GitHub 儲存庫路徑！")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    # ─── 題型二：情境問答（⚡ 欄位名 KeyError 終極修正完成版 ───
    elif speaking_sub == "情境問答":
        try:
            with open("data/speaking_situations.json", "r", encoding="utf-8") as f:
                speaking_situation_db = json.load(f)
        except FileNotFoundError:
            st.error("☠️ 系統性毀滅異常：偵測到 `data/speaking_situations.json` 檔案遺失，請確認是否建立！")
            speaking_situation_db = []

        if speaking_situation_db:
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown("### 🗣️ 口說測驗 - 情境問答")
            
            if "s_random_order" not in st.session_state:
                st.session_state.s_random_order = list(range(len(speaking_situation_db)))
                random.shuffle(st.session_state.s_random_order)
            if "s_pointer" not in st.session_state:
                st.session_state.s_pointer = 0
            if "s_show_q_trans" not in st.session_state:
                st.session_state.s_show_q_trans = {}
            if "s_show_ans" not in st.session_state:
                st.session_state.s_show_ans = {}
                
            s_ptr = st.session_state.s_pointer
            
            if s_ptr < len(speaking_situation_db):
                true_s_id = st.session_state.s_random_order[s_ptr]
                current_s_quiz = speaking_situation_db[true_s_id]
                
                if true_s_id not in st.session_state.s_show_q_trans:
                    st.session_state.s_show_q_trans[true_s_id] = False
                if true_s_id not in st.session_state.s_show_ans:
                    st.session_state.s_show_ans[true_s_id] = False
                    
                st.write(f"**當前進度：第 {s_ptr + 1} 題 / 共 {len(speaking_situation_db)} 題 (隨機題組模式)**")
                
                # 🛠️ 終極修補補丁：將 ['question_text'] 精準校正為對齊獨立題庫格式的 ['question_text'] 欄位，徹底根除 KeyError!
                st.markdown(f"#### ❓ 問：{current_s_quiz['question_text']}")
                
                # 題目的性質分類放在題目下方用較小的字註記
                st.markdown(f'<div class="category-note">性質分類：{current_s_quiz["category_note"]}</div>', unsafe_allow_html=True)
                
                # ─── 1. 題目中文意思雙向開關 ───
                s_q_trans_label = "🔄 關閉中文意思" if st.session_state.s_show_q_trans[true_s_id] else "👁️ 顯示中文意思"
                if st.button(s_q_trans_label, key=f"s_q_trans_btn_{s_ptr}"):
                    st.session_state.s_show_q_trans[true_s_id] = not st.session_state.s_show_q_trans[true_s_id]
                    st.rerun()
                    
                if st.session_state.s_show_q_trans[true_s_id]:
                    st.info(f"💡 中文意思：{current_s_quiz['question_ch']}")
                
                st.write("---")
                
                # ─── 2. 參考答案雙向開關鎖 ───
                s_ans_label = "🔄 關閉參考答案" if st.session_state.s_show_ans[true_s_id] else "📥 顯示參考答案"
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button(s_ans_label, key=f"s_ans_btn_{s_ptr}"):
                        st.session_state.s_show_ans[true_s_id] = not st.session_state.s_show_ans[true_s_id]
                        st.rerun()
                        
                with col2:
                    if st.session_state.s_show_ans[true_s_id]:
                        # 顯示參考答案：阿美語在上，中文翻譯在下
                        st.success(f"✨ **參考答案 (阿美語)：**\n\n{current_s_quiz['suggested_answer_amis']}\n\n"
                                   f"───\n\n💡 **中文翻譯：**\n\n{current_s_quiz['suggested_answer_ch']}")
                        
                if st.session_state.s_show_ans[true_s_id]:
                    st.write("")
                    # 留存參考音檔播放器位置（目前暫時留空）
                    st.caption("🔊 參考答案語音音檔 (製作中，目前暫時留空)")
                    
                    st.write("")
                    if st.button("➡️ 下一題", key=f"s_next_{s_ptr}"):
                        st.session_state.s_pointer += 1
                        st.rerun()
            else:
                st.balloons()
                st.success("🎉 恭喜！您已完成全部口說情境問答的隨機練習！")
                if st.button("🔄 重新挑戰", key="reset_speaking_situations"):
                    st.session_state.s_pointer = 0
                    if "s_show_ans" in st.session_state:
                        del st.session_state["s_show_ans"]
                    if "s_show_q_trans" in st.session_state:
                        del st.session_state["s_show_q_trans"]
                    random.shuffle(st.session_state.s_random_order)
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)
            
    elif speaking_sub == "看圖表達":
        st.markdown("### 🖼️ 看圖表達")
        st.warning("🚧 【內容建置中】")

# 4. 📖 閱讀測驗
elif current_tab == "📖 閱讀":
    st.subheader("📖 閱讀測驗 (Piasipan)")
    st.divider()
    reading_sub = st.radio(
        "閱讀題型選擇：",
        ["選擇題-詞彙語意", "選擇題-語言結構"],
        horizontal=True
    )
    
    try:
        with open("data/reading_quiz.json", "r", encoding="utf-8") as f:
            all_reading_data = json.load(f)
    except FileNotFoundError:
        st.error("☠️ 系統性毀滅異常：偵測到 `data/reading_quiz.json` 檔案遺失，請確認檔案是否已放置於 data/ 資料夾。")
        all_reading_data = []

    if all_reading_data:
        target_type = "vocabulary" if reading_sub == "選擇題-詞彙語意" else "structure"
        reading_db = [item for item in all_reading_data if item["type"] == target_type]
        
        state_order_key = f"r_{target_type}_order"
        state_ptr_key = f"r_{target_type}_ptr"
        state_opts_key = f"r_{target_type}_opts_map"
        state_submit_key = f"r_{target_type}_submit_map"
        state_choice_key = f"r_{target_type}_choice_map"
        
        if state_order_key not in st.session_state:
            st.session_state[state_order_key] = list(range(len(reading_db)))
            random.shuffle(st.session_state[state_order_key])
            
        if state_ptr_key not in st.session_state:
            st.session_state[state_ptr_key] = 0
            
        if state_opts_key not in st.session_state:
            st.session_state[state_opts_key] = {}
            
        if state_submit_key not in st.session_state:
            st.session_state[state_submit_key] = {}
            
        if state_choice_key not in st.session_state:
            st.session_state[state_choice_key] = {}

        r_ptr = st.session_state[state_ptr_key]
        
        if r_ptr < len(reading_db):
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            
            true_r_id = st.session_state[state_order_key][r_ptr]
            current_r_quiz = reading_db[true_r_id]
            
            if true_r_id not in st.session_state[state_submit_key]:
                st.session_state[state_submit_key][true_r_id] = False
            if true_r_id not in st.session_state[state_choice_key]:
                st.session_state[state_choice_key][true_r_id] = None
                
            if true_r_id not in st.session_state[state_opts_key]:
                shuffled_raw_opts = current_r_quiz["options"].copy()
                random.shuffle(shuffled_raw_opts)
                
                formatted_opts = []
                correct_text_formatted = ""
                correct_word_raw = current_r_quiz["correct_text"]
                
                for i, word_item in enumerate(shuffled_raw_opts):
                    display_text = f"({i+1}) {word_item}"
                    formatted_opts.append(display_text)
                    if word_item == correct_word_raw:
                        correct_text_formatted = display_text
                        
                st.session_state[state_opts_key][true_r_id] = {
                    "options": formatted_opts,
                    "correct_text": correct_text_formatted
                }
                
            live_r_data = st.session_state[state_opts_key][true_r_id]
            
            st.write(f"**當前進度：第 {r_ptr + 1} 題 / 共 {len(reading_db)} 題 (隨機出題組模式)**")
            st.write(current_r_quiz["question_text"])
            st.write("---")
            
            saved_choice = st.session_state[state_choice_key][true_r_id]
            saved_index = live_r_data["options"].index(saved_choice) if saved_choice in live_r_data["options"] else None
            
            user_r_choice = st.radio(
                "請選出正確的選項：",
                options=live_r_data["options"],
                index=saved_index,
                key=f"r_radio_{target_type}_{r_ptr}",
                disabled=st.session_state[state_submit_key][true_r_id]
            )
            
            if not st.session_state[state_submit_key][true_r_id]:
                st.session_state[state_choice_key][true_r_id] = user_r_choice
            
            if not st.session_state[state_submit_key][true_r_id]:
                if st.button("📥 提交答案", key=f"r_submit_btn_{target_type}_{r_ptr}"):
                    if user_r_choice is None:
                        st.warning("⚠️ 請先選擇一個選項再行提交！")
                    else:
                        st.session_state[state_submit_key][true_r_id] = True
                        st.rerun()
            else:
                correct_ans_str = live_r_data["correct_text"]
                if user_r_choice == correct_ans_str:
                    st.markdown(f"### 🔴 答題結果：✓")
                    st.success(f" Fangcal! 正確答案：**{correct_ans_str}**")
                else:
                    st.markdown(f"### 🔴 答題結果：✕")
                    st.error(f" 再接再厲！正確答案：**{correct_ans_str}**")
            
            st.write("")
            
            nav_col1, nav_col2 = st.columns(2)
            with nav_col1:
                if st.button("⬅️ 上一題", key=f"r_prev_btn_{target_type}_{r_ptr}", disabled=(r_ptr == 0)):
                    st.session_state[state_ptr_key] -= 1
                    st.rerun()
            with nav_col2:
                if st.button("➡️ 下一題", key=f"r_next_btn_{target_type}_{r_ptr}"):
                    st.session_state[state_ptr_key] += 1
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.balloons()
            st.success(f"🎉 恭喜！您已完成本項目全部 {len(reading_db)} 道隨機題組練習！")
            if st.button("🔄 重新洗牌挑戰", key=f"r_reset_{target_type}"):
                random.shuffle(st.session_state[state_order_key])
                st.session_state[state_ptr_key] = 0
                st.session_state[state_opts_key] = {}
                st.session_state[state_submit_key] = {}
                st.session_state[state_choice_key] = {}
                st.rerun()

# 5. ✍️ 寫作測驗
elif current_tab == "✍️ 寫作":
    st.subheader("✍️ 寫作測驗 (Pitilidan)")
    st.divider()
    writing_sub = st.radio(
        "寫作題型選擇：",
        ["句子聽寫", "問答"],
        horizontal=True
    )
    
    try:
        with open("data/writing_quiz.json", "r", encoding="utf-8") as f:
            all_writing_data = json.load(f)
    except FileNotFoundError:
        st.error("☠️ 系統性毀滅異常：偵測到 `data/writing_quiz.json` 檔案遺失，請檢查儲存庫路徑！")
        all_writing_data = []

    if all_writing_data:
        if writing_sub == "句子聽寫":
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown("### ✍️ 寫作測驗 - 句子聽寫")
            
            dictation_db = [item for item in all_writing_data if item["type"] == "dictation"]
            
            if "writing_dictation_order" not in st.session_state:
                st.session_state.writing_dictation_order = list(range(len(dictation_db)))
                random.shuffle(st.session_state.writing_dictation_order)
                
            if "writing_pointer" not in st.session_state:
                st.session_state.writing_pointer = 0
            if "writing_audio_triggered" not in st.session_state:
                st.session_state.writing_audio_triggered = False
            if "writing_submitted" not in st.session_state:
                st.session_state.writing_submitted = False

            w_ptr = st.session_state.writing_pointer
            
            if w_ptr < len(dictation_db):
                true_w_id = st.session_state.writing_dictation_order[w_ptr]
                current_w_quiz = dictation_db[true_w_id]
                
                st.write(f"**當前進度：第 {w_ptr + 1} 題 / 共 {len(dictation_db)} 題**")
                st.write(current_w_quiz["question_text"])
                
                if st.button("🔊 播放題目", key=f"w_play_{w_ptr}"):
                    st.session_state.writing_audio_triggered = True
                
                if st.session_state.writing_audio_triggered:
                    if os.path.exists(current_w_quiz["audio_path"]):
                        st.audio(current_w_quiz["audio_path"], format="audio/mp3", autoplay=True)
                    else:
                        st.error(f"⚠️ 找不到音檔！請確認此檔案是否已正確上傳至 GitHub 儲存庫：\n`{current_w_quiz['audio_path']}`")
                    st.session_state.writing_audio_triggered = False
                
                st.write("---")
                
                user_typed_answer = st.text_input(
                    "請在此輸入聽到的完整族語句子（注意大小寫與標點符號）：",
                    placeholder="請輸入答案...",
                    key=f"w_input_{w_ptr}",
                    disabled=st.session_state.writing_submitted
                )
                
                if not st.session_state.writing_submitted:
                    if st.button("📥 提交答案", key=f"w_submit_{w_ptr}"):
                        if not user_typed_answer.strip():
                            st.warning("⚠️ 請先在輸入框打字再行提交！")
                        else:
                            st.session_state.writing_submitted = True
                            st.rerun()
                else:
                    correct_sentence = current_w_quiz["correct_text"]
                    
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.button("📥 提交答案", key=f"w_sub_dis_{w_ptr}", disabled=True)
                    with col2:
                        st.info(f"💡 正確答案：**{correct_sentence}**")
                    
                    st.write("")
                    if st.button("➡️ 下一題", key=f"w_next_{w_ptr}"):
                        st.session_state.writing_pointer += 1
                        st.session_state.writing_submitted = False
                        st.rerun()
            else:
                st.balloons()
                st.success("🎉 您已完成本輪全部 5 道隨機聽寫題目！")
                if st.button("🔄 開始下一輪隨機挑戰", key="reset_writing"):
                    random.shuffle(st.session_state.writing_dictation_order)
                    st.session_state.writing_pointer = 0
                    st.session_state.writing_submitted = False
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif writing_sub == "問答":
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown("### 📝 寫作測驗 - 問答")
            
            question_db = [item for item in all_writing_data if item["type"] == "question"]
            
            if "q_pointer" not in st.session_state:
                st.session_state.q_pointer = 0
            if "q_audio_triggered" not in st.session_state:
                st.session_state.q_audio_triggered = False
            if "q_submitted" not in st.session_state:
                st.session_state.q_submitted = False

            q_ptr = st.session_state.q_pointer
            
            if q_ptr < len(question_db):
                current_q_quiz = question_db[q_ptr]
                
                if "q_show_trans" not in st.session_state:
                    st.session_state.q_show_trans = {}
                if "q_show_ans" not in st.session_state:
                    st.session_state.q_show_ans = {}
                    
                if q_ptr not in st.session_state.q_show_trans:
                    st.session_state.q_show_trans[q_ptr] = False
                if q_ptr not in st.session_state.q_show_ans:
                    st.session_state.q_show_ans[q_ptr] = False
                
                st.write(f"**當前進度：第 {q_ptr + 1} 題 / 共 {len(question_db)} 題**")
                st.markdown(f"#### ❓ 問：{current_q_quiz['question_text']}")
                
                trans_btn_label = "🔄 關閉中文翻譯" if st.session_state.q_show_trans[q_ptr] else "👁️ 顯示中文翻譯"
                if st.button(trans_btn_label, key=f"q_trans_toggle_{q_ptr}"):
                    st.session_state.q_show_trans[q_ptr] = not st.session_state.q_show_trans[q_ptr]
                    st.rerun()
                
                if st.session_state.q_show_trans[q_ptr]:
                    st.info(f"💡 中文提示：{current_q_quiz['chinese_translation']}")
                
                st.write("---")
                
                ans_btn_label = "🔄 關閉參考答案" if st.session_state.q_show_ans[q_ptr] else "📥 顯示參考答案"
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button(ans_btn_label, key=f"q_ans_toggle_{q_ptr}"):
                        st.session_state.q_show_ans[q_ptr] = not st.session_state.q_show_ans[q_ptr]
                        st.rerun()
                
                with col2:
                    if st.session_state.q_show_ans[q_ptr]:
                        suggested_ans = current_q_quiz["suggested_answer"]
                        st.success(f"✨ 參考答案：**{suggested_ans}**")
                
                if st.session_state.q_show_ans[q_ptr]:
                    st.write("")
                    if st.button("🔊 播放參考答案音檔", key=f"q_audio_btn_{q_ptr}"):
                        st.session_state.q_audio_triggered = True
                        
                    if st.session_state.q_audio_triggered:
                        if os.path.exists(current_q_quiz["audio_path"]):
                            st.audio(current_q_quiz["audio_path"], format="audio/mp3", autoplay=True)
                        else:
                            st.error(f"⚠️ 找不到音檔！請確認此檔案是否已正確上傳至 GitHub 儲存庫：\n`{current_q_quiz['audio_path']}`")
                        st.session_state.q_audio_triggered = False
                    
                    st.write("")
                    if st.button("➡️ 下一題", key=f"q_next_{q_ptr}"):
                        st.session_state.q_pointer += 1
                        st.rerun()
            else:
                st.success("🎉 您已完成「問答」全部題目的練習！")
                if st.button("🔄 重新挑戰", key="reset_questions"):
                    st.session_state.q_pointer = 0
                    if "q_show_trans" in st.session_state:
                        del st.session_state["q_show_trans"]
                    if "q_show_ans" in st.session_state:
                        del st.session_state["q_show_ans"]
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)

# ---- App 底部註腳 ----
st.write("---")
st.caption("© 2026 中高級認證 App 三一開發團隊 ｜ 雙重隨機全防禦穩定版")
