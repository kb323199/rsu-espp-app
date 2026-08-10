# RSU / ESPP 估值計算器

> 供台灣員工計算美股股權報酬（RSU / ESPP）台幣所得的 Web 應用程式

🔗 **線上網址**：https://rsu-espp-app.onrender.com

---

## 功能總覽

### 使用者系統
- 帳號註冊 / 登入 / 登出
- 計算紀錄綁定個人帳號，不同使用者彼此隔離

### RSU 計算
- 輸入授予日期、美股代號、股數
- 自動抓取授予日**前一交易日**收盤價（Yahoo Finance）
- 自動抓取當日美金/台幣匯率（台灣銀行）
- 計算台幣總價值 = 收盤價 × 股數 × 匯率

### ESPP 計算
- 認購日限 1/31 或 7/31
- 自動依 ESPP 規則抓取兩個參考日股價
    - **參考日 A**:認購日前一交易日(遇週末往前跳到週五)
    - **參考日 B**:期初日(1/31 認購取前一年 8/1、7/31 認購取當年 2/1)前一交易日
- 成本價 = min(參考A, 參考B) × 85%
- 所得 = (參考A - 成本價) × 股數 × 匯率

### 紀錄管理
- 歷史紀錄列表（含台幣總計）
- 單筆刪除紀錄
- 清空所有紀錄
- 匯出 CSV（Excel 開啟中文不亂碼）
- 匯出 Excel（含格式化標題列）

---

## 技術架構

| 項目 | 技術 |
|------|------|
| 後端 | Python Flask |
| 使用者認證 | Flask-Login + Werkzeug |
| 資料庫（開發）| SQLite |
| 資料庫（生產）| PostgreSQL (Supabase) |
| 股價來源 | Yahoo Finance API v8（免費，無需 API Key）|
| 匯率來源 | 台灣銀行網頁即時匯率 |
| 部署平台 | Render |
| Excel 匯出 | openpyxl |

---

## 本機開發

### 1. 安裝套件
```bash
pip install -r requirements.txt
```

### 2. 啟動
```bash
python app.py
```

瀏覽器開啟：http://localhost:5000

> 本機使用 SQLite（`entries.db`），不需設定資料庫。

---

## 部署到 Render

### 環境變數設定

| 變數名稱 | 說明 |
|----------|------|
| `DATABASE_URL` | Supabase PostgreSQL 連線字串 |
| `SECRET_KEY` | Flask session 加密金鑰（任意字串） |

### 部署步驟
1. Fork 或 Push 到 GitHub
2. Render → New Web Service → 連結 GitHub repo
3. 設定環境變數
4. 啟動指令：`gunicorn app:app`（已寫入 Procfile）

---

## 專案結構

```
rsu-espp-app/
├── app.py              # 主程式（路由、資料庫、計算邏輯）
├── requirements.txt    # Python 套件清單
├── Procfile            # Render 啟動指令
├── project prompt.md   # 專案起始 Prompt 說明
├── README.md
└── templates/
    ├── index.html      # 主頁（計算 + 紀錄列表）
    ├── login.html      # 登入頁
    └── register.html   # 註冊頁
```

---

## requirements.txt

```
Flask>=2.0
gunicorn>=20.0
psycopg2-binary>=2.9
Flask-Login>=0.6
Werkzeug>=2.0
openpyxl>=3.0
```
