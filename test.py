# 建立一個模擬的產品測試紀錄清單 (List)
npi_logs = [
    "PASS: 批次A_測試正常",
    "ERROR: 批次B_探針卡接觸不良",
    "PASS: 批次C_測試正常",
    "ERROR: 批次D_阻抗過高"
]

print("--- 開始分析測試紀錄 ---")

# 使用迴圈 (For loop) 與 條件判斷 (If/Else) 來分類異常
anomaly_count = 0

for log in npi_logs:
    if "ERROR" in log:
        print(f"⚠️ 發現異常: {log}")
        anomaly_count += 1
    else:
        print(f"✅ 正常: {log}")

print("-" * 25)
print(f"分析結束，共發現 {anomaly_count} 筆異常aaa")
