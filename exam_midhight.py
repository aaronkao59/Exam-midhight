import streamlit as st
import random
import json
import os

# ---- 1. 頁面佈局設定 ----
st.set_page_config(page_title="中高級認證", page_icon="🎓", layout="centered", initial_sidebar_state="collapsed")

# ---- 2. CSS 設計 ----
st.markdown("""
    <style>
    .quiz-card { background-color: var(--secondary-background-color); padding: 24px; border-radius: 16px; border: 1px solid rgba(128, 128, 128, 0.2); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); margin-top: 15px; margin-bottom: 25px; }
    h1, h2, h3 { color: #0D9488 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 中高級認證")
st.caption("[練習平台 選擇器]")

main_options = ["📋 認證考試說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
current_tab = st.segmented_control("主選單導覽", main_options, default="📋 認證考試說明", label_visibility="collapsed")

# 🧠 跨頁面狀態解耦
if "previous_tab" not in st.session_state: st.session_state.previous_tab = current_tab
if st.session_state.previous_tab != current_tab:
    st.session_state.previous_tab = current_tab
    st.rerun()

# ---- 聽力題庫定義 ----
QUIZ_DATA = [
    {"id": 1, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-01.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["riyar", "'alo", "fanaw", "sa'owac"], "correct_text": "riyar"},
    {"id": 2, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-02.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["korkor", "rohayan", "romakat", "rotarot"], "correct_text": "romakat"}
]

# ---- 🗣️ 口說測驗邏輯 ----
if current_tab == "🗣️ 口說":
    st.subheader("🗣️ 口說測驗 (Pisowalan)")
    speaking_sub = st.radio("口說題型選擇：", ["段落朗讀", "情境問答", "看圖表達"], horizontal=True)
    
    if speaking_sub == "情境問答":
        try:
            with open("data/speaking_situations.json", "r", encoding="utf-8") as f:
                db = json.load(f)
        except:
            db = []
            st.error("題庫讀取失敗")

        if db:
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            mode = st.radio("練習模式：", ["🎲 隨機挑戰題目", "📋 自由選擇題組"], horizontal=True, key="s_mode")
            
            if "s_random_order" not in st.session_state:
                st.session_state.s_random_order = list(range(len(db)))
                random.shuffle(st.session_state.s_random_order)
            if "s_pointer" not in st.session_state: st.session_state.s_pointer = 0
            
            if mode == "🎲 隨機挑戰題目":
                idx = st.session_state.s_pointer % len(db)
                true_id = st.session_state.s_random_order[idx]
                st.write(f"當前進度：第 {idx + 1} 題 / 共 {len(db)} 題")
            else:
                true_id = st.selectbox("請選擇題組：", range(len(db)), format_func=lambda x: f"第 {x+1} 題")
            
            quiz = db[true_id]
            
            if st.button("🔊 播放題目語音音檔"):
                fid = str(quiz['quiz_id']).zfill(2)
                path = f"speaking_qa/situation_{fid}.mp3"
                if os.path.exists(path):
                    st.audio(path, format="audio/mp3", autoplay=True)
                else:
                    st.warning(f"💡 音檔製作中: {path}")

            if "show_q" not in st.session_state: st.session_state.show_q = False
            if "show_t" not in st.session_state: st.session_state.show_t = False
            if "show_a" not in st.session_state: st.session_state.show_a = False
            
            col1, col2 = st.columns(2)
            if col1.button("👁️ 顯示/隱藏族語"): st.session_state.show_q = not st.session_state.show_q
            if col2.button("👁️ 顯示/隱藏中文"): st.session_state.show_t = not st.session_state.show_t
            
            if st.session_state.show_q: st.info(quiz['question_amis'])
            if st.session_state.show_t: st.markdown(f"> {quiz['question_ch']}")
            
            if st.button("📥 顯示/隱藏參考答案"): st.session_state.show_a = not st.session_state.show_a
            if st.session_state.show_a:
                st.success(f"阿美語參考：\n{quiz['suggested_answer_amis']}\n\n中文參考：\n{quiz['suggested_answer_ch']}")
            
            if mode == "🎲 隨機挑戰題目" and st.button("➡️ 下一題"):
                st.session_state.s_pointer += 1
                st.session_state.show_q = False
                st.session_state.show_t = False
                st.session_state.show_a = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
    elif speaking_sub == "看圖表達":
        st.info("看圖表達功能運作中...")

# ---- 📖 閱讀測驗 ----
elif current_tab == "📖 閱讀":
    st.subheader("📖 閱讀測驗 (Piasipan)")
    # ... (省略部分代碼以維持回應長度，請保留您原有的閱讀測驗區塊)

# ---- ✍️ 寫作測驗 ----
elif current_tab == "✍️ 寫作":
    st.subheader("✍️ 寫作測驗 (Pitilidan)")
    # ... (此處保留寫作測驗的邏輯)

# ---- App 底部 ----
st.write("---")
st.caption("© 2026 中高級認證 App 三一開發團隊")
