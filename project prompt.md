# RSU / ESPP 估值計算器 ── 最佳起始 Prompt

## 📌 如果一開始就用這個 Prompt，可以最有效率地完成整個專案

---

## 🚀 建議的起始 Prompt（直接複製貼給 AI）

```
請幫我用 Python Flask 建立一個「RSU / ESPP 股票估值計算器」Web 應用程式，
供台灣上市公司員工計算美股股權報酬的台幣所得。

## 功能需求

### 使用者系統
- 使用者註冊（帳號 + 密碼，密碼加密儲存）
- 使用者登入 / 登出
- 所有計算紀錄綁定登入帳號，不同使用者彼此隔離

### RSU 計算功能
- 輸入：授予日期（yyyy-mm-dd）、美股代號（如 MU）、股數
- 自動抓取：授予日前一個交易日的收盤股價（Yahoo Finance API）
- 自動抓取：授予日前一個交易日的美金/台幣匯率（台灣銀行網頁，若為今日則抓即時）
- 計算：台幣總價值 = 收盤價 × 股數 × 匯率

### ESPP 計算功能
- 輸入：認購日期（只能是 1/31 或 7/31）、美股代號、股數
- ESPP 認購規則：
  - 1/31 認購：參考A = 當年1/31前一交易日股價，參考B = 前一年8/1前一交易日股價
  - 7/31 認購：參考A = 當年7/31前一交易日股價，參考B = 當年2/1前一交易日股價
  - 成本價 = min(參考A, 參考B) × 85%
  - 所得價 = max(參考A, 參考B)
  - 所得 = (所得價 - 成本價) × 股數 × 匯率

### 資料儲存
- 本機開發：SQLite（entries.db）
- 雲端部署：PostgreSQL（透過 DATABASE_URL 環境變數自動切換）
- 資料表：users（帳號密碼）、entries（計算紀錄，含 user_id 外鍵）

### 紀錄管理
- 顯示該使用者所有歷史計算紀錄（表格）
- 顯示所有紀錄的台幣總計
- 清空所有紀錄（只清除該使用者）
- 匯出 CSV（UTF-8 BOM，Excel 開啟中文不亂碼）
- 匯出 Excel（含藍色標題列格式，欄寬自動調整）

### 前端介面
- RSU / ESPP 用 Tab 切換
- 響應式設計（支援手機）
- 登入狀態顯示於頂部導覽列，含登出按鈕
- 計算成功 / 失敗顯示訊息

### 部署
- 部署平台：Render（免費方案）
- 資料庫：Supabase PostgreSQL（免費方案）
- 環境變數：DATABASE_URL、SECRET_KEY
- 啟動指令：gunicorn app:app（Procfile）

## 技術選型
- 後端：Python Flask
- 登入：Flask-Login + Werkzeug（密碼 hash）
- 資料庫：SQLite（開發）/ PostgreSQL psycopg2（生產）
- 前端：純 HTML + CSS（不使用前端框架，保持簡單）
- 股價 API：Yahoo Finance v8（不需 API key）
- 匯率來源：台灣銀行 https://rate.bot.com.tw/xrt?Lang=zh-TW

## 專案結構
rsu-espp-app/
├── app.py           # 主程式（路由、資料庫、計算邏輯）
├── requirements.txt
├── Procfile
└── templates/
    ├── index.html   # 主頁（RSU/ESPP 計算 + 紀錄列表）
    ├── login.html
    └── register.html

請先建立完整的 app.py 與所有 templates，確保本機可以 python app.py 直接執行。
```

---

## 💡 為什麼這樣寫最有效率？

| 原因 | 說明 |
|------|------|
| **一次給完所有需求** | 避免來回補充，AI 能一次生成完整架構 |
| **明確技術選型** | 指定 Flask、psycopg2、Flask-Login，不讓 AI 自己選可能不熟悉的套件 |
| **說明部署環境** | 提前說明 Render + Supabase，AI 會自動處理環境變數切換邏輯 |
| **說明資料庫切換邏輯** | 本機 SQLite / 雲端 PostgreSQL 雙模式，開發部署都方便 |
| **給清楚的商業規則** | ESPP 計算規則複雜，直接描述演算法，避免 AI 猜錯邏輯 |
| **指定專案結構** | AI 生成的檔案結構符合預期，不需要事後重整 |
| **要求可直接執行** | 明確說「本機可直接執行」，AI 會確保不缺少 init_db 等初始化邏輯 |

---

## ⚠️ 本專案實際走過的彎路（新手參考）

| 問題 | 根本原因 | 如果一開始就做對 |
|------|---------|----------------|
| 登入後 500 error | PostgreSQL 舊資料表缺 `user_id` 欄位 | 一開始就設計含 user_id 的 schema |
| CSV 中文亂碼 | 缺少 UTF-8 BOM | 一開始就加 `'\ufeff'` |
| git 指令失敗 | 在錯誤目錄執行 git | 養成 `cd` 到專案目錄的習慣 |
| pip 安裝失敗 | 公司內網 PyPI 有 SSL 問題 | 加 `--index-url https://pypi.org/simple/ --trusted-host` |
| `#` 欄位不從1開始 | 顯示資料庫 ID 而非列序號 | template 用 `{{ loop.index }}` 而非 `{{ row.id }}` |

---

## 📦 完整 requirements.txt

```
Flask>=2.0
gunicorn>=20.0
psycopg2-binary>=2.9
Flask-Login>=0.6
Werkzeug>=2.0
openpyxl>=3.0
```
