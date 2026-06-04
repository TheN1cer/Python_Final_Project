import matplotlib.pyplot as plt
from wordcloud import WordCloud
# 讓使用者輸入檔案路徑
file_path = input("請輸入檔案名稱: ")

try:
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    print(f"成功讀取檔案: {file_path}")
except FileNotFoundError:
    print("找不到該檔案，請檢查名稱是否正確。")
    exit(1)

#清理標點符號及換行符號, punctuation包含了所有的標點符號。
import string
text = text.translate(str.maketrans("", "", string.punctuation))

# 2. 文字切割 (將字串轉為 List)
word_list = text.split()

# 3. 過濾雜訊 (設定 Tuple 黑名單)
stop_words = ("is", "and", "the", "a", "of", "to", "in", "that", "it", "with", "as", "for", "was", "on", "are", "by", "this", "be", "or", "from", "at", "which", "but", "not", "all", "we", "they", "their", "his", "her", "my", "your", "its", "me", "him", "you", "i", "has", "have", "do", "does", "did", "he", "she", "them", "what", "who", "when", "where", "why", "how")
filtered_words = []
for word in word_list:
    # 簡單的清理：將單字轉小寫，方便比對
    clean_word = word.lower()
    if clean_word not in stop_words:
        filtered_words.append(clean_word)

# 4. 統計次數 (使用 Dict)
word_counts = {}
for word in filtered_words:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1

# 5. 排序並輸出結果
result = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

# 6. 改為取前 20 筆資料
limit = 30
filtered_result = result[:limit]  # 利用切片 [start:stop]

print(f"出現次數最多的前 {limit} 個關鍵字:")
for word, count in filtered_result:
    print(f"{word:<12}: {count}次")

# 檢查是否還有資料
if len(filtered_result) > 0:
    # 拆解成繪圖用的 lists
    words, values = map(list, zip(*filtered_result))
    
    # --- 繪製長條圖 ---
    plt.figure(figsize=(10, 6))
    plt.bar(words, values, color='skyblue')
    plt.title(f"Top {limit} Keywords")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout() # 自動調整邊界，避免標籤被切掉
    plt.savefig("bar_chart.png")
    print("長條圖已儲存為 bar_chart.png")

    # --- 繪製文字雲 ---
    # 使用 generate_from_frequencies 直接接收統計字典
    wc = WordCloud(width=1920, height=1080, background_color='white', colormap='inferno')
    wc.generate_from_frequencies(word_counts)
    
    plt.figure(figsize=(16, 9))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig("wordcloud.png", dpi=120, bbox_inches='tight')
    print("文字雲已儲存為 wordcloud.png")
    
else:
    print("沒有找到達到門檻的關鍵字，無法繪圖。")


