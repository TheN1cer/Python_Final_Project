import streamlit as st
import os
import pandas as pd
from Final_project import TextAnalyzer 

# 網頁寬螢幕配置
st.set_page_config(page_title="Python 文本分析", page_icon="📝", layout="wide")

st.title("📝 Python 文本分析")
st.markdown("上傳您的 `.txt` 或 `.pdf` 檔案，系統將自動進行資料篩選、字頻統計，並產出數據報告！")

# --- 畫面左側：側邊欄設定區 ---
with st.sidebar:
    st.header("⚙️ 分析設定")
    
    # 數量設定滑桿
    limit_slider = st.slider("選擇圖表顯示的關鍵字數量", min_value=5, max_value=50, value=20, step=5)
    
    st.divider()
    
    # 【新功能】點子二：自訂停用詞輸入框
    st.subheader("🧹 文字過濾")
    custom_stopwords = st.text_input(
        "輸入要排除的字 (以英文逗號隔開):", 
        placeholder="例如: also, however, columns"
    )

# --- 畫面中央：檔案上傳區 ---
uploaded_file = st.file_uploader("請上傳要分析的文檔", type=['txt', 'pdf'])

if uploaded_file is not None:
    if st.button("🚀 開始分析文檔", type="primary"):
        with st.spinner('系統分析中...'):
            
            # 建立暫存實體檔案
            temp_file_path = f"temp_{uploaded_file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            # 實例化分析機
            analyzer = TextAnalyzer()
            
            # 執行流程
            if analyzer.load_file(temp_file_path):
                # 將側邊欄輸入的自訂字串傳給後台
                analyzer.process_text(custom_stopwords_str=custom_stopwords)
                analyzer.generate_reports(limit=limit_slider)
                
                st.success("🎉 分析順利完成！")
                
                # --- 【新功能】點子一：文章數據體檢儀表板 ---
                if analyzer.filtered_words:
                    total_words = len(analyzer.filtered_words)
                    unique_words = len(analyzer.word_counts)
                    richness = (unique_words / total_words) * 100
                    
                    # 建立三個精美的並排指標卡
                    m1, m2, m3 = st.columns(3)
                    m1.metric("總字數", f"{total_words:,} 字")
                    m2.metric("不重複單字數", f"{unique_words:,} 個")
                    m3.metric("詞彙豐富度", f"{richness:.1f} %")
                
                st.divider()

                # --- 數據分頁展示區 ---
                tab1, tab2 = st.tabs(["📊 分析圖表", "📋 數據報表"])
                
                with tab1:
                    # 分開呈現兩張大圖，上下排列，寬度填滿
                    st.markdown("### 📊 關鍵字頻率長條圖")
                    if os.path.exists("bar_chart.png"):
                        st.image("bar_chart.png", use_container_width=True)
                    
                    st.divider()
                    
                    st.markdown("### ☁️ 關鍵字雲")
                    if os.path.exists("wordcloud.png"):
                        st.image("wordcloud.png", use_container_width=True)
                
                with tab2:
                    st.markdown("### 📋 字頻統計數據表")
                    if os.path.exists("keyword_report.csv"):
                        df = pd.read_csv("keyword_report.csv")
                        st.dataframe(df, use_container_width=True)
                        
                        # 下載按鈕
                        with open("keyword_report.csv", "rb") as file:
                            st.download_button(
                                label="📥 下載完整 CSV 統計報表",
                                data=file,
                                file_name="keyword_report.csv",
                                mime="text/csv",
                            )

            # 任務完成，移除暫存檔
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)