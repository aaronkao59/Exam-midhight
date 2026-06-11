import streamlit as st

# ---- 頁面佈局設定 ----
st.set_page_config(
    page_title="中高級認證 App 模擬器",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---- 自動適應雙模式的 CSS 設計 ----
# 這裡使用 Streamlit 的原生變數，當使用者切換系統明暗時，顏色會自動變白或變黑
# 同時保持精緻的框線與元件質感
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
    
    /* 標題與重點文字：使用亮眼且百搭的青色（Teal），在明暗模式下都有極佳的閱讀性 */
    h1, h2, h3 {
        color: #0D9488 !important; /* 調整為明暗皆宜的深青色 */
    }
    
    /* 當處於暗黑模式時，微調標題顏色使其更亮眼 */
    @media (prefers-color-scheme: dark) {
        h1, h2, h3 {
            color: #2DD4BF !important; /* 亮青色 */
        }
    }
    
    /* 調整副標題與說明文字的顏色透明度，確保層級分明 */
    .stMarkdown p {
        color: var(--text-color);
        opacity: 0.85;
    }
    
    /* 提示區塊的自訂微調 */
    .stAlert {
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---- App 頂部導覽列 ----
st.title("🎓 中高級認證")
st.caption("族語認證數位學習平台 ｜ 自動適應明暗模式 UI")
st.write("---")

# ---- 第一層：五個主要選項 (導覽選單) ----
# segmented_control 在 Streamlit 官方原生設計中就完美支援雙模式切換
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
    
    💡 **介面更新提示：**
    * 本界面已導入動態主題變數。
    * 您可以點擊 Streamlit 右上角的 **三條線選單 ➔ Settings ➔ Theme** 手動切換 Light/Dark 模式，測試視覺效果！
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
        st.warning("🚧 【內容建置中】此處未來將播放單詞音檔，並提供選項供使用者辨識詞根。")
        st.button("播放音檔 🔊", disabled=True)
        
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
st.caption("© 2026 中高級認證 App 開發團隊 ｜ 雙模式 UI 測試版")
