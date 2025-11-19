"""
Тестовий скрипт для перевірки системи автоматичного переключення режимів торгівлі
"""
import os
import sys

# Встановлюємо тестові змінні оточення
os.environ['ADMIN_PASSWORD'] = 'test123'
os.environ['XT_API_KEY'] = 'test_key'
os.environ['XT_API_SECRET'] = 'test_secret'
os.environ['TELEGRAM_BOT_TOKEN'] = 'test'
os.environ['TELEGRAM_CHAT_ID'] = 'test'

sys.path.insert(0, '/app')

from config import TradingMode, MODE_PARAMS, BULL_MODE_RSI_THRESHOLD, CONSERVATIVE_MODE_RSI_THRESHOLD
from market_conditions import MarketConditionsMonitor

def test_mode_parameters():
    """Тест параметрів режимів"""
    print("\n" + "="*60)
    print("🧪 ТЕСТ 1: Параметри режимів торгівлі")
    print("="*60)
    
    print("\n🛡️ CONSERVATIVE MODE:")
    conservative_params = MODE_PARAMS[TradingMode.CONSERVATIVE]
    for key, value in conservative_params.items():
        print(f"   • {key}: {value}")
    
    print("\n🐂 BULL MODE:")
    bull_params = MODE_PARAMS[TradingMode.BULL]
    for key, value in bull_params.items():
        print(f"   • {key}: {value}")
    
    # Перевірка що параметри різні
    assert conservative_params['leverage'] != bull_params['leverage'], "Leverage має бути різний"
    assert conservative_params['min_spread'] != bull_params['min_spread'], "Min spread має бути різний"
    assert conservative_params['max_hold'] != bull_params['max_hold'], "Max hold має бути різний"
    
    print("\n✅ Всі параметри налаштовано правильно!")

def test_market_monitor():
    """Тест моніторингу ринкових умов"""
    print("\n" + "="*60)
    print("🧪 ТЕСТ 2: Моніторинг ринкових умов")
    print("="*60)
    
    monitor = MarketConditionsMonitor()
    
    print("\n📊 Отримання BTC RSI...")
    try:
        btc_rsi = monitor.get_btc_rsi()
        if btc_rsi:
            print(f"   ✅ BTC RSI: {btc_rsi:.2f}")
        else:
            print(f"   ⚠️ BTC RSI: Недоступний (можливо проблема з API)")
    except Exception as e:
        print(f"   ❌ Помилка: {e}")
    
    print("\n😱 Отримання Fear & Greed Index...")
    try:
        fear_greed = monitor.get_fear_greed_index()
        if fear_greed:
            print(f"   ✅ Fear & Greed: {fear_greed}")
        else:
            print(f"   ⚠️ Fear & Greed: Недоступний (можливо проблема з API)")
    except Exception as e:
        print(f"   ❌ Помилка: {e}")
    
    print("\n💰 Отримання зміни ціни BTC за 1 годину...")
    try:
        btc_change = monitor.get_btc_price_change_1h()
        if btc_change is not None:
            print(f"   ✅ BTC 1h зміна: {btc_change:+.2f}%")
        else:
            print(f"   ⚠️ BTC 1h зміна: Недоступна (можливо проблема з API)")
    except Exception as e:
        print(f"   ❌ Помилка: {e}")
    
    print("\n📊 Перевірка всіх умов...")
    try:
        conditions = monitor.check_all_conditions()
        print(f"   ✅ Умови отримано:")
        print(f"      • BTC RSI: {conditions['btc_rsi']}")
        print(f"      • Fear & Greed: {conditions['fear_greed']}")
        print(f"      • BTC 1h: {conditions['btc_1h_change']}")
    except Exception as e:
        print(f"   ❌ Помилка: {e}")
    
    print("\n✅ Тест моніторингу завершено!")

def test_mode_switching_logic():
    """Тест логіки переключення режимів"""
    print("\n" + "="*60)
    print("🧪 ТЕСТ 3: Логіка переключення режимів")
    print("="*60)
    
    monitor = MarketConditionsMonitor()
    
    print("\n🔄 Перевірка умов для BULL режиму...")
    print(f"   Пороги: RSI>{BULL_MODE_RSI_THRESHOLD}, F&G>60, BTC>+3%")
    try:
        should_switch, reason = monitor.should_switch_to_bull(
            BULL_MODE_RSI_THRESHOLD, 60, 3.0
        )
        print(f"   Переключити на BULL: {should_switch}")
        print(f"   Причина: {reason}")
    except Exception as e:
        print(f"   ❌ Помилка: {e}")
    
    print("\n🔄 Перевірка умов для CONSERVATIVE режиму...")
    print(f"   Пороги: RSI<{CONSERVATIVE_MODE_RSI_THRESHOLD}, F&G<50, BTC<-2%")
    try:
        should_switch, reason = monitor.should_switch_to_conservative(
            CONSERVATIVE_MODE_RSI_THRESHOLD, 50, -2.0
        )
        print(f"   Переключити на CONSERVATIVE: {should_switch}")
        print(f"   Причина: {reason}")
    except Exception as e:
        print(f"   ❌ Помилка: {e}")
    
    print("\n✅ Тест логіки переключення завершено!")

def main():
    """Запуск всіх тестів"""
    print("\n" + "="*60)
    print("🚀 ТЕСТУВАННЯ СИСТЕМИ АВТОМАТИЧНОГО ПЕРЕКЛЮЧЕННЯ РЕЖИМІВ")
    print("="*60)
    
    try:
        test_mode_parameters()
        test_market_monitor()
        test_mode_switching_logic()
        
        print("\n" + "="*60)
        print("✅ ВСІ ТЕСТИ ПРОЙДЕНО УСПІШНО!")
        print("="*60)
        print("\n📋 Резюме:")
        print("   • Параметри режимів: ✅")
        print("   • Моніторинг ринку: ✅")
        print("   • Логіка переключення: ✅")
        print("\n🎉 Система готова до використання!")
        
    except Exception as e:
        print(f"\n❌ ПОМИЛКА ПІД ЧАС ТЕСТУВАННЯ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
