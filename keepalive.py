"""
Supabase 保活腳本。

Supabase 免費方案的專案若超過 7 天沒有任何資料庫活動就會自動暫停（pause）。
這支腳本只是連上資料庫跑一個最輕量的查詢（SELECT 1），讓 Supabase 判定
專案仍在使用中，藉此避免被自動暫停。搭配 .github/workflows/keep-supabase-alive.yml
排程執行，不需要人工登入。

需要環境變數 DATABASE_URL（與 app.py / Render 上設定的值相同）。
"""

import os
import sys

import psycopg2


def main() -> int:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("錯誤：未設定 DATABASE_URL 環境變數", file=sys.stderr)
        return 1

    # 與 app.py 相同的相容處理
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    try:
        conn = psycopg2.connect(database_url, connect_timeout=10)
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
            conn.commit()
        finally:
            conn.close()
    except Exception as exc:  # noqa: BLE001 — 保活腳本需要捕捉任何連線錯誤並回報
        print(f"連線資料庫失敗：{exc}", file=sys.stderr)
        return 1

    print("Supabase 保活查詢成功。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
