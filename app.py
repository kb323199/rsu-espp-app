from datetime import date, datetime, timedelta
import json
import re
import sqlite3
import urllib.error
import urllib.parse
import urllib.request

import os

from flask import Flask, g, redirect, render_template, request, url_for

DATABASE = "entries.db"
app = Flask(__name__)

VALID_TICKER_RE = re.compile(r"^[A-Za-z0-9\.\-]{1,10}$")


def get_db():
    db = getattr(g, "db", None)
    if db is None:
        db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        g.db = db
    return db


@app.teardown_appcontext
def close_db(exc):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trade_date TEXT NOT NULL,
            ticker TEXT NOT NULL,
            shares REAL NOT NULL,
            close_price REAL NOT NULL,
            usd_twd REAL NOT NULL,
            value_usd REAL,
            value_twd REAL NOT NULL,
            source TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    # Ensure `value_usd` column exists for older databases
    cur = db.execute("PRAGMA table_info(entries)")
    cols = [r[1] for r in cur.fetchall()]
    if "value_usd" not in cols:
        try:
            db.execute("ALTER TABLE entries ADD COLUMN value_usd REAL")
        except Exception:
            pass
    db.commit()


def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("日期格式須為 yyyy-mm-dd")


def http_get_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        raw = response.read().decode("utf-8", errors="ignore")
    return json.loads(raw)


def fetch_yahoo_close_price(symbol, target_date):
    start_dt = datetime.combine(target_date - timedelta(days=10), datetime.min.time())
    end_dt = datetime.combine(target_date + timedelta(days=1), datetime.min.time())
    period1 = int(start_dt.timestamp())
    period2 = int(end_dt.timestamp())
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}"
        f"?period1={period1}&period2={period2}&interval=1d&includePrePost=false"
    )
    data = http_get_json(url)
    result = data.get("chart", {}).get("result")
    if not result:
        raise ValueError(f"無法取得 {symbol} 的資料")
    quote = result[0].get("indicators", {}).get("quote", [])
    timestamps = result[0].get("timestamp", [])
    if not quote or not timestamps:
        raise ValueError(f"{symbol} 無歷史交易資料")
    closes = quote[0].get("close", [])
    best_price = None
    best_timestamp = None
    for ts, close in zip(timestamps, closes):
        if close is None:
            continue
        current = date.fromtimestamp(ts)
        if current <= target_date:
            if best_timestamp is None or current > date.fromtimestamp(best_timestamp):
                best_timestamp = ts
                best_price = close
    if best_price is None:
        raise ValueError(f"{symbol} 在指定日或之前沒有可用收盤價")
    return best_price, date.fromtimestamp(best_timestamp)


def fetch_usd_twd_rate_for_today():
    url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        html = response.read().decode("utf-8", errors="ignore")
    usd_rows = re.findall(r"<tr.*?>.*?</tr>", html, re.S)
    for row in usd_rows:
        if "美金" in row and "(USD)" in row:
            numbers = re.findall(r"<td[^>]*>\s*([0-9.,]+)\s*</td>", row)
            if numbers:
                buy_rate = numbers[0].replace(",", "")
                return float(buy_rate)
    raise ValueError("無法解析台灣銀行匯率資料")


def fetch_usd_twd_rate(symbol, target_date):
    if target_date == date.today():
        try:
            return fetch_usd_twd_rate_for_today(), "台灣銀行本行買入"
        except Exception:
            pass
    price, actual_date = fetch_yahoo_close_price(symbol, target_date)
    return price, "Yahoo 匯率"


@app.route("/", methods=["GET", "POST"])
def index():
    init_db()
    error = None
    message = None
    if request.method == "POST":
        trade_date = request.form.get("trade_date", "").strip()
        ticker = request.form.get("ticker", "").strip().upper()
        shares = request.form.get("shares", "").strip()
        if not trade_date or not ticker or not shares:
            error = "請填寫完整的日期、美股代號與股數。"
        elif not VALID_TICKER_RE.match(ticker):
            error = "股票代號格式不正確。"
        else:
            try:
                trade_date_obj = parse_date(trade_date)
                if trade_date_obj > date.today():
                    raise ValueError("日期錯誤：不能選擇未來日期")
                shares_value = float(shares)
                if shares_value <= 0:
                    raise ValueError("股數必須大於 0")
                close_price, stock_date = fetch_yahoo_close_price(ticker, trade_date_obj)
                usd_twd_rate, rate_source = fetch_usd_twd_rate("USDTWD=X", trade_date_obj)
                value_twd = round(close_price * shares_value * usd_twd_rate, 2)
                db = get_db()
                value_usd = round(close_price * shares_value, 4)
                db.execute(
                    "INSERT INTO entries (trade_date, ticker, shares, close_price, usd_twd, value_usd, value_twd, source, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        trade_date_obj.isoformat(),
                        ticker,
                        shares_value,
                        round(close_price, 4),
                        round(usd_twd_rate, 4),
                        value_usd,
                        value_twd,
                        f"股票 {ticker}({stock_date}) / 匯率 {rate_source}",
                        datetime.now().isoformat(timespec="seconds"),
                    ),
                )
                db.commit()
                message = f"已新增 {ticker} 的計算結果，總價值 {value_twd:,} TWD。"
            except Exception as exc:
                error = str(exc)
    db = get_db()
    rows_raw = db.execute("SELECT * FROM entries ORDER BY id DESC").fetchall()
    processed_rows = []
    for row in rows_raw:
        value_twd = float(row["value_twd"]) if row["value_twd"] is not None else 0.0
        value_usd = float(row["value_usd"]) if ("value_usd" in row.keys() and row["value_usd"] is not None) else value_twd / float(row["usd_twd"]) if row["usd_twd"] else 0.0
        processed_rows.append(
            {
                "id": row["id"],
                "trade_date": row["trade_date"],
                "ticker": row["ticker"],
                "shares": row["shares"],
                "close_price": row["close_price"],
                "usd_twd": row["usd_twd"],
                "value_twd": row["value_twd"],
                "value_usd": value_usd,
                "source": row["source"],
                "value_formatted": f"{value_twd:,.2f}",
                "value_usd_formatted": f"{value_usd:,.2f}",
            }
        )
    total = sum(r["value_twd"] for r in rows_raw) if rows_raw else 0.0
    total_formatted = f"{total:,.2f}"
    return render_template(
        "index.html",
        rows=processed_rows,
        total=round(total, 2),
        total_formatted=total_formatted,
        error=error,
        message=message,
    )


@app.route("/clear", methods=["POST"])
def clear_entries():
    init_db()
    db = get_db()
    # Drop and recreate the table to guarantee AUTOINCREMENT resets to 1
    try:
        db.execute("DROP TABLE IF EXISTS entries")
        db.commit()
    except Exception:
        db.rollback()
    # Recreate table schema
    init_db()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Initialize the database within an application context so `g` is available
    with app.app_context():
        init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
