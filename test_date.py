from datetime import date, timedelta

def get_last_trading_day_before(d):
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    d -= timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d

# 2026/1/31 是週六 → 預期往前2天 → 1/29 週四
d = date(2026, 1, 31)
print(f"{d} 是 {['一','二','三','四','五','六','日'][d.weekday()]}，參考日 → {get_last_trading_day_before(d)}")

# 2027/1/31 是週日 → 預期往前3天 → 1/28 週四
d = date(2027, 1, 31)
print(f"{d} 是 {['一','二','三','四','五','六','日'][d.weekday()]}，參考日 → {get_last_trading_day_before(d)}")

# 2025/1/31 是週五 → 預期往前1天 → 1/30 週四
d = date(2025, 1, 31)
print(f"{d} 是 {['一','二','三','四','五','六','日'][d.weekday()]}，參考日 → {get_last_trading_day_before(d)}")

# 2025/7/31 是週四 → 預期往前1天 → 7/30 週三
d = date(2025, 7, 31)
print(f"{d} 是 {['一','二','三','四','五','六','日'][d.weekday()]}，參考日 → {get_last_trading_day_before(d)}")