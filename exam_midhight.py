import streamlit as st
import random
import json
import os

# ---- 頁面設定 ----
st.set_page_config(page_title="中高級認證", page_icon="🎓", layout="centered", initial_sidebar_state="collapsed")

# ---- CSS 設計 ----
st.markdown("""
    <style>
    .quiz-card { background-color: var(--secondary-background-color); padding: 24px; border-radius: 16px; border: 1px solid rgba(128, 128, 128, 0.2); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); margin-top: 15px; margin-bottom: 25px; }
    h1, h2, h3 { color: #0D9488 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 中高級認證")
st.caption("練習平台 選擇器")

# ---- 選單 ----
main_options = ["📋 認證考試說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
current_tab = st.segmented_control("主選單導覽", main_options, default="📋 認證考試說明", label_visibility="collapsed")

if "previous_tab" not in st.session_state: st.session_state.previous_tab = current_tab
if st.session_state.previous_tab != current_tab:
    st.session_state.previous_tab = current_tab
    st.rerun()

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
                    st.warning(f"💡 音檔製作中 (路徑: {path})")

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
        try:
            with open("data/speaking_images.json", "r", encoding="utf-8") as f:
                img_db = json.load(f)
        except:
            img_db = []
            
        if img_db:
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            title = st.selectbox("主題選擇：", [item["title"] for item in img_db])
            quiz = next(item for item in img_db if item["title"] == title)
            
            if os.path.exists(quiz["image_path"]):
                st.image(quiz["image_path"], use_container_width=True)
            
            if "show_d" not in st.session_state: st.session_state.show_d = False
            if st.button("📝 顯示/隱藏草稿區"): st.session_state.show_d = not st.session_state.show_d
            if st.session_state.show_d: st.text_area("草稿區", key=f"draft_{quiz['quiz_id']}")
            
            if st.button("📥 顯示/隱藏參考答案"): st.session_state.show_ia = not st.session_state.get("show_ia", False)
            if st.session_state.get("show_ia"):
                st.success(f"參考答案：\n{quiz['suggested_answer_amis']}\n\n中文：{quiz['suggested_answer_ch']}")
            st.markdown('</div>', unsafe_allow_html=True)

# ---- ✍️ 寫作測驗 ----
elif current_tab == "✍️ 寫作":
    st.subheader("✍️ 寫作測驗")
    sub = st.radio("題型：", ["句子聽寫", "問答"], horizontal=True)
    
    if sub == "問答":
        try:
            with open("data/writing_quiz.json", "r", encoding="utf-8") as f:
                all_data = json.load(f)
            q_db = [item for item in all_data if item["type"] == "question"]
        except:
            q_db = []
            
        if q_db:
            if "q_p" not in st.session_state: st.session_state.q_p = 0
            idx = st.session_state.q_p % len(q_db)
            quiz = q_db[idx]
            
            st.markdown(f"#### 問：{quiz['question_text']}")
            if st.button("👁️ 顯示中文"): st.session_state.show_q_trans = not st.session_state.get("show_q_trans", False)
            if st.session_state.get("show_q_trans"): st.info(quiz['chinese_translation'])
            
            st.text_input("輸入答案進行練習：")
            
            if st.button("📥 顯示/隱藏參考答案"): st.session_state.show_q_ans = not st.session_state.get("show_q_ans", False)
            if st.session_state.get("show_q_ans"): st.success(quiz['suggested_answer'])
            
            if st.button("➡️ 下一題"):
                st.session_state.q_p += 1
                st.rerun()

st.write("---")
st.caption("© 2026 中高級認證 App")
