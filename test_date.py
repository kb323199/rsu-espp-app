from datetime import date, timedelta

def get_prev_trading_day(d):
    """
    取得指定日期的前一個交易日：
    - 平日(週一~週五) → 往前1天
    - 週六 → 往前2天
    - 週日 → 往前3天
    """
    wd = d.weekday()
    if wd == 5:    # 週六
        d -= timedelta(days=2)
    elif wd == 6:  # 週日
        d -= timedelta(days=3)
    else:          # 週一~週五
        d -= timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d

days = ['一','二','三','四','五','六','日']

print("=== 1/31 認購日：參考A=1/31前一交易日，參考B=前一年8/1前一交易日 ===")

# 2025/1/31 週四 → 往前1天 → 1/30 週三
d = date(2025, 1, 31)
print(f"參考A: {d} 是週{days[d.weekday()]}，收盤參考日 → {get_prev_trading_day(d)}")
# 前一年 8/1: 2024/8/1 週四 → 往前1天 → 7/31 週三
d2 = date(2024, 8, 1)
print(f"參考B: {d2} 是週{days[d2.weekday()]}，收盤參考日 → {get_prev_trading_day(d2)}")

print()
# 2026/1/31 週六 → 往前2天 → 1/29 週四
d = date(2026, 1, 31)
print(f"參考A: {d} 是週{days[d.weekday()]}，收盤參考日 → {get_prev_trading_day(d)}")
# 前一年 8/1: 2025/8/1 週五 → 往前1天 → 7/31 週四
d2 = date(2025, 8, 1)
print(f"參考B: {d2} 是週{days[d2.weekday()]}，收盤參考日 → {get_prev_trading_day(d2)}")

print()
# 2027/1/31 週日 → 往前3天 → 1/28 週四
d = date(2027, 1, 31)
print(f"參考A: {d} 是週{days[d.weekday()]}，收盤參考日 → {get_prev_trading_day(d)}")
# 前一年 8/1: 2026/8/1 週六 → 往前2天 → 7/30 週四
d2 = date(2026, 8, 1)
print(f"參考B: {d2} 是週{days[d2.weekday()]}，收盤參考日 → {get_prev_trading_day(d2)}")

print()
print("=== 7/31 認購日：參考A=7/31前一交易日，參考B=前一年2/1前一交易日 ===")

# 2025/7/31 週四 → 往前1天 → 7/30 週三
d = date(2025, 7, 31)
print(f"參考A: {d} 是週{days[d.weekday()]}，收盤參考日 → {get_prev_trading_day(d)}")
# 前一年 2/1: 2024/2/1 週四 → 往前1天 → 1/31 週三
d2 = date(2024, 2, 1)
print(f"參考B: {d2} 是週{days[d2.weekday()]}，收盤參考日 → {get_prev_trading_day(d2)}")

print()
# 2026/7/31 週五 → 往前1天 → 7/30 週四
d = date(2026, 7, 31)
print(f"參考A: {d} 是週{days[d.weekday()]}，收盤參考日 → {get_prev_trading_day(d)}")
# 前一年 2/1: 2025/2/1 週六 → 往前2天 → 1/30 週四
d2 = date(2025, 2, 1)
print(f"參考B: {d2} 是週{days[d2.weekday()]}，收盤參考日 → {get_prev_trading_day(d2)}")