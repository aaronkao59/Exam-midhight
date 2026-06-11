import streamlit as st

# ---- 頁面佈局與風格設定 ----
st.set_page_config(
    page_title="中高級認證 App 模擬器",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自訂 CSS 讓介面更像手機 App 的高質感深色風格
st.markdown("""
    <style>
    .main {
        background-color: #0F172A;
    }
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 15px;
    }
    h1, h2, h3 {
        color: #14B8A6 !important;
    }
    p {
        color: #94A3B8;
    }
    </style>
""", unsafe_allow_html=True)

# ---- App 頂部導覽列 ----
st.title("🎓 中高級認證")
st.caption("族語認證數位學習平台 ｜ 模擬視覺介面")
st.write("---")

# ---- 第一層：五個主要選項 (導覽選單) ----
# 使用 segmented_control 模擬 App 的底部分頁或主要切換頁籤
main_options = ["📋 測驗說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
current_tab = st.segmented_control(
    "主選單導覽", 
    main_options, 
    default="📋 測驗說明",
    label_visibility="collapsed"
)

st.write("") # 留空行增加視覺舒適度

# ---- 第二層：根據選擇顯示對應架構 ----

# 1. 測驗說明頁面
if current_tab == "📋 測驗說明":
    st.subheader("📋 測驗說明 (Pacihanan)")
    st.markdown("""
    歡迎使用**中高級認證學習 App**！本系統專為族語中高級認證測驗設計。
    
    💡 **使用指南：**
    * 請點選上方切換 **聽力**、**口說**、**閱讀**、**寫作** 四大模組。
    * 目前架構已設定完成，內容將於後續更新中陸續添加。
    """)
    st.info("📌 目前進度：系統基礎骨架建置完成，等待題庫導入。")

# 2. 聽力模組
elif current_tab == "🎧 聽力":
    st.subheader("🎧 聽力模組 (Pitengilan)")
    st.write("請選擇下方的題型開始練習：")
    
    # 第二層選項
    listening_sub = st.radio(
        "聽力題型選擇：",
        ["選擇題-聽音選詞", "選擇題-對話理解"],
        horizontal=True
    )
    
    if listening_sub == "選擇題-聽音選詞":
        st.markdown("### 🔍 選擇題 - 聽音選詞")
        st.warning("🚧 【內容建置中】此處未來將播放單詞音檔，並提供選項供使用者辨識詞根。")
        # 預留未來互動元件空間
        st.button("播放音檔 🔊", disabled=True)
        
    elif listening_sub == "選擇題-對話理解":
        st.markdown("### 💬 選擇題 - 對話理解")
        st.warning("🚧 【內容建置中】此處未來將播放部落生活情境對話，並測試長句理解能力。")

# 3. 口說模組
elif current_tab == "🗣️ 口說":
    st.subheader("🗣️ 口說模組 (Pisowalan)")
    st.write("請選擇下方的題型開始練習：")
    
    # 第二層選項
    speaking_sub = st.radio(
        "口說題型選擇：",
        ["段落朗讀", "情境問答", "看圖表達"],
        horizontal=True
    )
    
    if speaking_sub == "段落朗讀":
        st.markdown("### 📖 段落朗讀")
        st.warning("🚧 【內容建置中】未來將呈現祭典、神話等短文段落，引導精準發音與喉塞音校準。")
        
    elif speaking_sub == "情境問答":
        st.markdown("### ❓ 情境問答")
        st.warning("🚧 【內容建置中】未來將由系統隨機語音提問，訓練 VSO 語序的即時應答。")
        
    elif speaking_sub == "看圖表達":
        st.markdown("### 🖼️ 看圖表達")
        st.warning("🚧 【內容建置中】未來將顯示文化情境圖片，引導進行結構性的口頭敘事。")

# 4. 閱讀模組
elif current_tab == "📖 閱讀":
    st.subheader("📖 閱讀模組 (Piasipan)")
    st.write("請選擇下方的題型開始練習：")
    
    # 第二層選項
    reading_sub = st.radio(
        "閱讀題型選擇：",
        ["選擇題-詞彙語意", "選擇題-語言結構"],
        horizontal=True
    )
    
    if reading_sub == "選擇題-詞彙語意":
        st.markdown("### 🏷️ 選擇題 - 詞彙語意")
        st.warning("🚧 【內容建置中】預計整合權威辭典鎖定，測試中高級核心詞彙之延伸語意。")
        
    elif reading_sub == "選擇題-語言結構":
        st.markdown("### ⛓️ 選擇題 - 語言結構")
        st.warning("🚧 【內容建置中】聚焦於焦點系統 (Focus System) 與複雜時態變化的語法測試。")

# 5. 寫作模組
elif current_tab == "✍️ 寫作":
    st.subheader("✍️ 寫作模組 (Pitilidan)")
    st.write("請選擇下方的題型開始練習：")
    
    # 第二層選項
    writing_sub = st.radio(
        "寫作題型選擇：",
        ["句子聽寫", "問答"],
        horizontal=True
    )
    
    if writing_sub == "句子聽寫":
        st.markdown("### ✍️ 句子聽寫")
        st.warning("🚧 【內容建置中】播放標準語音，使用者需正確輸入符合正字法規範的族語句子。")
        st.text_input("請輸入聽到的句子（預留輸入框）：", placeholder="內容添加後即可輸入...", disabled=True)
        
    elif writing_sub == "問答":
        st.markdown("### 📝 問答")
        st.warning("🚧 【內容建置中】針對特定文化或社會議題，進行中長篇幅的書面論述撰寫。")
        st.text_area("請寫下您的回答（預留文字區域）：", placeholder="內容添加後即可輸入...", disabled=True)

# ---- App 底部註腳 ----
st.write("---")
st.caption("© 2026 中高級認證 App 開發團隊 ｜ 暫時架構建置版")