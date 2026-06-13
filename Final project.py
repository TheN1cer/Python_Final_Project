import string
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pdfplumber

# ==========================================
# 定義藍圖：文字分析器類別 (對應 p7 OOP 觀念)
# ==========================================
class TextAnalyzer:
    def __init__(self):
        """
        建構子 (Constructor)：初始化物件的屬性。
        每當我們建立一個新的分析器物件，這些專屬的變數就會被初始化。
        """
        self.text = ""             # 用來存放讀取進來的原始文章字串
        self.word_counts = {}       # 用來存放統計完的單字字典
        
        # 停用詞常數，做為物件的專屬常數屬性容器 (Tuple)
        self.stop_words = (
            "is", "and", "the", "a", "of", "to", "in", "that", "it", "with", 
            "as", "for", "was", "on", "are", "by", "this", "be", "or", "from", 
            "at", "which", "but", "not", "all", "we", "they", "their", "his", 
            "her", "my", "your", "its", ""
        )

    def load_file(self, file_path):
        """
        方法：讀取檔案 (支援 TXT 與 PDF)，並將結果寫入 self.text (對應 p4 File I/O)
        """
        self.text = ""  # 每次讀新檔案時先清空舊資料
        try:
            if file_path.lower().endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text = file.read()
                print(f"【系統提示】成功讀取 TXT 檔案: {file_path}")
                return True

            elif file_path.lower().endswith(".pdf"):
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text: 
                            self.text += page_text + "\n"
                print(f"【系統提示】成功讀取 PDF 檔案: {file_path} (共 {len(pdf.pages)} 頁)")
                return True
            else:
                print("【錯誤】格式錯誤！目前本系統僅支援 .txt 或 .pdf 格式。")
                return False

        except FileNotFoundError:
            print("【錯誤】找不到該檔案，請檢查名稱與路徑。")
            return False
        except Exception as e:
            print(f"【錯誤】讀取檔案時發生異常: {e}")
            return False

    def process_text(self):
        """
        方法：負責文字清洗、過濾與字頻統計，並存入 self.word_counts (對應 p5 容器型別)
        """
        if not self.text:
            print("【警告】目前無文字資料，請先成功執行 load_file() 讀取檔案。")
            return

        # 1. 資料清洗
        clean_text = self.text.translate(str.maketrans("", "", string.punctuation)).replace("\n", " ")
        word_list = clean_text.split(" ")

        # 2. 過濾停用詞
        filtered_words = []
        for word in word_list:
            clean_word = word.lower().strip()
            if clean_word not in self.stop_words:
                filtered_words.append(clean_word)

        # 3. 使用 Dict 統計次數
        self.word_counts = {}
        for word in filtered_words:
            if word in self.word_counts:
                self.word_counts[word] += 1
            else:
                self.word_counts[word] = 1
        print("【系統提示】資料預處理與統計完成。")

    def generate_reports(self, limit=20):
        """
        方法：將數據表格化與視覺化輸出 (對應 p9 Pandas & p10 Matplotlib)
        """
        if not self.word_counts:
            print("【警告】尚未進行文字統計，無法產生報告。")
            return

        # 1. 排序與進階字長過濾 (利用切片撈出前 N 筆)
        sorted_result = sorted(self.word_counts.items(), key=lambda x: x[1], reverse=True)
        top_words = [item for item in sorted_result if len(item[0]) > 2][:limit]

        if len(top_words) == 0:
            print("【提示】過濾後無符合條件的關鍵字。")
            return

        # 2. 導入 Pandas 結構化數據並匯出 CSV
        df = pd.DataFrame(top_words, columns=['Keyword', 'Frequency'])
        print(f"\n======================================")
        print(f"   出現次數最多的前 {limit} 個關鍵字排名")
        print(f"======================================")
        print(df.to_string(index=False))
        print(f"======================================\n")

        df.to_csv("keyword_report.csv", index=False, encoding="utf-8-sig")
        print("📊 Excel 報表已匯出為: keyword_report.csv")

        # 3. 使用 Matplotlib 雙子圖繪製綜合儀表板
        words = df['Keyword'].tolist()
        values = df['Frequency'].tolist()
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # [左邊長條圖]
        axes[0].bar(words, values, color='skyblue')
        axes[0].set_title(f"Top {limit} Keywords Bar Chart", fontsize=14)
        axes[0].set_xlabel("Words")
        axes[0].set_ylabel("Frequency")
        axes[0].tick_params(axis='x', rotation=45)
        
        # [右邊文字雲]
        wc = WordCloud(width=800, height=600, background_color='white', colormap='viridis')
        wc.generate_from_frequencies(self.word_counts)
        
        axes[1].imshow(wc, interpolation='bilinear')
        axes[1].axis('off')
        axes[1].set_title("Keyword Word Cloud", fontsize=14)
        
        # 儲存儀表板
        plt.tight_layout()
        plt.savefig("Analysis_Dashboard.png")
        print("🎨 視覺化儀表板已匯出為: Analysis_Dashboard.png")


# ==========================================
# 主程式執行區塊 (CLI 互動選單)
# ==========================================
if __name__ == "__main__":
    # 1. 實例化：打造一台我們的文字分析機
    analyzer = TextAnalyzer()
    
    # 預設的顯示數量
    current_limit = 20  

    # 2. 無窮迴圈：讓選單持續顯示，直到使用者選擇離開
    while True:
        print("\n" + "="*35)
        print("      📝 Python 文本分析")
        print("="*35)
        print("  1. 讀取並分析新檔案 (TXT/PDF)")
        print(f"  2. 調整圖表顯示的單字數量 (目前: {current_limit} 筆)")
        print("  3. 輸出 Excel 報表與視覺化儀表板")
        print("  4. 離開系統")
        print("="*35)
        
        # 接收使用者輸入
        choice = input("👉 請選擇功能 (1-4): ")

        # 3. 控制結構：依據使用者的選擇，呼叫分析機對應的按鈕 (Methods)
        if choice == '1':
            file_name = input("請輸入檔案名稱 (支援 .txt 或 .pdf): ")
            # 如果讀檔成功，就順便幫使用者自動「清洗與統計」
            if analyzer.load_file(file_name):
                analyzer.process_text()
                
        elif choice == '2':
            try:
                new_limit = int(input("請輸入新的顯示數量 (例如 10 或 50): "))
                if new_limit > 0:
                    current_limit = new_limit
                    print(f"【系統提示】顯示數量已成功更新為 {current_limit} 筆。")
                else:
                    print("【錯誤】數量必須大於 0 喔！")
            except ValueError:
                print("【錯誤】請輸入有效的整數！")
                
        elif choice == '3':
            # 防呆機制：如果根本還沒讀檔(字典是空的)，就不能產圖
            if not analyzer.word_counts:
                print("【警告】你還沒有分析任何檔案！請先選擇功能「1」。")
            else:
                analyzer.generate_reports(limit=current_limit)
                
        elif choice == '4':
            print("👋 再見！")
            break  # 打破 while 迴圈，結束程式
            
        else:
            print("【錯誤】無效的選項，請輸入 1 到 4 之間的數字。")