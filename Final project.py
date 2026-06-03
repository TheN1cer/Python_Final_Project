import matplotlib.pyplot as plt
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
text = text.translate(str.maketrans("", "", string.punctuation)).replace("\n", " ")

# 2. 文字切割 (將字串轉為 List)
word_list = text.split(" ")

# 3. 過濾雜訊 (設定 Tuple 黑名單)
stop_words = ("is", "and", "the", "a", "of", "to", "in", "that", "it", "with", "as", "for", "was", "on", "are", "by", "this", "be", "or", "from", "at", "which", "but", "not", "all", "we", "they", "their", "his", "her", "my", "your", "its")
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

# 6. 設定門檻並輸出 (使用 if 過濾)
threshold = 2
print(f"--- 關鍵字統計 (出現 {threshold} 次以上) ---")

for word, count in result:
    if count >= threshold:
        print(f"關鍵字: {word:<12} | 出現次數: {count}")
    else:
        # 因為 result 已經是從大到小排序，若遇到小於門檻的，後面的就都不用檢查了
        break

# 7. 繪製長條圖 (使用 Matplotlib)
words, values = map(list, zip(*result))
plt.bar(words, values)

# 加入標題與標籤 (這對期末報告非常重要)
plt.title("Keyword Frequency Analysis")
plt.xlabel("Words")
plt.ylabel("Frequency")

# 顯示或儲存圖表
plt.show()

input("按下 Enter 鍵以結束程式...")