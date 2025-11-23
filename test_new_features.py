#!/usr/bin/env python3
"""
Тест нових фіч:
1. Анті-шиткоїн фільтри
2. LONG захист від перегріву
3. Trailing stop
"""
import sys
import time
sys.path.insert(0, '/app')

from config import *
from bot import is_shitcoin, check_long_overheat

print("=" * 80)
print("ТЕСТ 1: АНТІ-ШИТКОЇН ФІЛЬТРИ")
print("=" * 80)

# Тест 1: Низька ліквідність (має бути заблоковано)
print("\n1.1. Токен з низькою ліквідністю:")
test_token_1 = {
    "liquidity": 50000,  # < 180,000
    "volume_24h": 3000000,
    "price_change_5m": 2.0,
    "price_change_1h": 5.0,
    "pairCreatedAt": (time.time() - 30 * 86400) * 1000  # 30 днів тому
}
result_1 = is_shitcoin("TEST1", test_token_1)
print(f"   Результат: {'❌ ЗАБЛОКОВАНО' if result_1 else '✅ ДОЗВОЛЕНО'} (очікується ❌)")

# Тест 2: Малий об'єм (має бути заблоковано)
print("\n1.2. Токен з малим об'ємом 24h:")
test_token_2 = {
    "liquidity": 200000,
    "volume_24h": 1000000,  # < 2,500,000
    "price_change_5m": 2.0,
    "price_change_1h": 5.0,
    "pairCreatedAt": (time.time() - 30 * 86400) * 1000
}
result_2 = is_shitcoin("TEST2", test_token_2)
print(f"   Результат: {'❌ ЗАБЛОКОВАНО' if result_2 else '✅ ДОЗВОЛЕНО'} (очікується ❌)")

# Тест 3: Висока волатильність 5м (має бути заблоковано)
print("\n1.3. Токен з високою волатильністю 5м:")
test_token_3 = {
    "liquidity": 200000,
    "volume_24h": 3000000,
    "price_change_5m": 10.0,  # > 8%
    "price_change_1h": 5.0,
    "pairCreatedAt": (time.time() - 30 * 86400) * 1000
}
result_3 = is_shitcoin("TEST3", test_token_3)
print(f"   Результат: {'❌ ЗАБЛОКОВАНО' if result_3 else '✅ ДОЗВОЛЕНО'} (очікується ❌)")

# Тест 4: Висока волатильність 1г (має бути заблоковано)
print("\n1.4. Токен з високою волатильністю 1г:")
test_token_4 = {
    "liquidity": 200000,
    "volume_24h": 3000000,
    "price_change_5m": 2.0,
    "price_change_1h": 40.0,  # > 35%
    "pairCreatedAt": (time.time() - 30 * 86400) * 1000
}
result_4 = is_shitcoin("TEST4", test_token_4)
print(f"   Результат: {'❌ ЗАБЛОКОВАНО' if result_4 else '✅ ДОЗВОЛЕНО'} (очікується ❌)")

# Тест 5: Молодий токен (має бути заблоковано)
print("\n1.5. Токен віком < 14 днів:")
test_token_5 = {
    "liquidity": 200000,
    "volume_24h": 3000000,
    "price_change_5m": 2.0,
    "price_change_1h": 5.0,
    "pairCreatedAt": (time.time() - 10 * 86400) * 1000  # 10 днів тому
}
result_5 = is_shitcoin("TEST5", test_token_5)
print(f"   Результат: {'❌ ЗАБЛОКОВАНО' if result_5 else '✅ ДОЗВОЛЕНО'} (очікується ❌)")

# Тест 6: Якісний токен (має бути дозволено)
print("\n1.6. Якісний токен:")
test_token_6 = {
    "liquidity": 500000,
    "volume_24h": 5000000,
    "price_change_5m": 2.0,
    "price_change_1h": 5.0,
    "pairCreatedAt": (time.time() - 30 * 86400) * 1000
}
result_6 = is_shitcoin("TEST6", test_token_6)
print(f"   Результат: {'❌ ЗАБЛОКОВАНО' if result_6 else '✅ ДОЗВОЛЕНО'} (очікується ✅)")

print("\n" + "=" * 80)
print("ТЕСТ 2: ЗАХИСТ ВІД ПЕРЕГРІВУ LONG ПОЗИЦІЙ")
print("=" * 80)

# Тест 7: Перегрітий токен для LONG (має бути заблоковано)
print("\n2.1. Перегрітий токен (зріст >6% за 5м):")
test_long_overheat_1 = {
    "price_change_5m": 7.5  # > 6%
}
result_7 = check_long_overheat(test_long_overheat_1, "LONG_TEST1")
print(f"   Результат: {'❌ LONG ЗАБЛОКОВАНО' if result_7 else '✅ LONG ДОЗВОЛЕНО'} (очікується ❌)")

# Тест 8: Нормальний токен для LONG (має бути дозволено)
print("\n2.2. Нормальний токен для LONG:")
test_long_overheat_2 = {
    "price_change_5m": 3.0  # < 6%
}
result_8 = check_long_overheat(test_long_overheat_2, "LONG_TEST2")
print(f"   Результат: {'❌ LONG ЗАБЛОКОВАНО' if result_8 else '✅ LONG ДОЗВОЛЕНО'} (очікується ✅)")

print("\n" + "=" * 80)
print("ТЕСТ 3: ПЕРЕВІРКА КОНФІГУРАЦІЇ TRAILING STOP")
print("=" * 80)

print("\n3.1. Параметри консервативного режиму:")
print(f"   Trailing stop: {MODE_PARAMS[TradingMode.CONSERVATIVE]['trailing']}% (очікується 0.5%)")
print(f"   Leverage: {MODE_PARAMS[TradingMode.CONSERVATIVE]['leverage']}x")
print(f"   Take Profit: {MODE_PARAMS[TradingMode.CONSERVATIVE]['tp']}%")
print(f"   Stop Loss: {MODE_PARAMS[TradingMode.CONSERVATIVE]['sl']}%")

print("\n3.2. Параметри bull режиму:")
print(f"   Trailing stop: {MODE_PARAMS[TradingMode.BULL]['trailing']}% (очікується 0.6%)")
print(f"   Leverage: {MODE_PARAMS[TradingMode.BULL]['leverage']}x")
print(f"   Take Profit: {MODE_PARAMS[TradingMode.BULL]['tp']}%")
print(f"   Stop Loss: {MODE_PARAMS[TradingMode.BULL]['sl']}%")

print("\n" + "=" * 80)
print("ТЕСТ 4: ПЕРЕВІРКА АНТІ-ШИТКОЇН ПАРАМЕТРІВ")
print("=" * 80)

print(f"\n4.1. Мін. ліквідність: ${ANTI_SHITCOIN_MIN_LIQUIDITY:,} (очікується $180,000)")
print(f"4.2. Мін. об'єм 24h: ${ANTI_SHITCOIN_MIN_VOLUME_24H:,} (очікується $2,500,000)")
print(f"4.3. Макс. волатильність 5м: {ANTI_SHITCOIN_MAX_VOLATILITY_5M}% (очікується 8%)")
print(f"4.4. Макс. волатильність 1г: {ANTI_SHITCOIN_MAX_VOLATILITY_1H}% (очікується 35%)")
print(f"4.5. Мін. вік токену: {ANTI_SHITCOIN_MIN_TOKEN_AGE_DAYS} днів (очікується 14)")
print(f"4.6. Поріг перегріву LONG: {LONG_OVERHEAT_THRESHOLD}% (очікується 6%)")

print("\n" + "=" * 80)
print("✅ ВСІ ТЕСТИ ЗАВЕРШЕНО!")
print("=" * 80)
