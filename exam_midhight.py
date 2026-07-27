import streamlit as st
import random
import json
import os

APP_VERSION = "v3.1.2 (Multicolor Neon UI - Light/Dark Optimized)"

st.set_page_config(page_title="中高級認證", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")

# ==============================================================================
# 🎨 介面視覺與交互架構 - [霓虹化設計補丁 v9.2]
# 首席介面視覺架構師 (Chief UIUX Architect) 簽核通過
# ==============================================================================
st.markdown("""
    <style>
    /* ========================================= */
    /* 1. 基礎卡片與佈局 (未更動) */
    /* ========================================= */
    .quiz-card {
        background-color: var(--secondary-background-color);
        padding: 24px; border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-top: 15px; margin-bottom: 25px;
    }
    .stAlert { border-radius: 12px !important; border: none !important; }
    div[data-testid="stHorizontalBlock"] { background: transparent !important; border: none !important; box-shadow: none !important; }

    /* ========================================= */
    /* 2. 標題霓虹化核心策略 - 全域定義 */
    /*適用於 h1, h2, h3 */
    /* ========================================= */
    h1, h2, h3 {
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        /* 使用漸層色彩作為背景並剪裁至文字 */
        background-image: linear-gradient(90deg, #ff00de, #00ffff, #fff000, #ff0000, #00ff00) !important;
        background-size: 200% auto !important;
        -webkit-background-clip: text !important;
        background-clip: text !important;
        
        /* 動畫效果：漸層滾動 */
        animation: neon_gradient_roll 10s linear infinite, neon_flicker 3s infinite alternate !important;
    }

    /* 漸層文字滾動動畫 */
    @keyframes neon_gradient_roll {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }

    /* 輕微霓虹閃爍動畫，增加真實感 */
    @keyframes neon_flicker {
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
            opacity: 1;
        }
        20%, 22%, 24%, 55% {
            opacity: 0.8;
        }
    }

    /* ========================================= */
    /* 3. 雙模式自適應策略 (ESS Mode Adaptation) */
    /* ========================================= */

    /* ☀️ [淺色模式 - Light Mode] 對比度優先協議 */
    @media (prefers-color-scheme: light) {
        h1, h2, h3 {
            /* 淺色模式文字色彩需加深，否則會因發光模糊 */
            color: rgba(0, 0, 0, 0.1) !important; /* 文字本體幾乎透明，靠漸層背景顯示 */
            
            /* 輕微、內斂的發光，確保不晃眼 */
            text-shadow: 
                0 0 1px #fff,
                0 0 3px #fff,
                1px 1px 3px rgba(13, 148, 136, 0.4) !important;
        }
    }

    /* 🌙 [深色模式 - Dark Mode] 發光與多巴胺全開協議 */
    @media (prefers-color-scheme: dark) {
        h1, h2, h3 {
            /* 深色模式文字色彩設為白，強化霓虹發光 */
            color: #fff !important;
            
            /* 多層級、擴散式霓虹文字陰影 */
            text-shadow: 
                0 0 5px #fff,               /* 核心發光 */
                0 0 10px #fff,              /* 霓虹燈管色彩層 */
                0 0 15px #00ffff,           /* 藍色擴散 */
                0 0 20px #00ffff,
                0 0 30px #ff00de,           /* 粉色擴散 */
                0 0 40px #ff00de,
                0 0 55px #fff000,           /* 黃色擴散 */
                0 0 75px #fff000 !important;
        }
    }
    </style>
""", unsafe_allow_html=True)
# ==============================================================================

@st.cache_data(show_spinner=False)
def load_json_data(file_path):
    # ...(以下 Python 邏輯完全未變動，省略)...
