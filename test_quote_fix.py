#!/usr/bin/env python3
"""
Тест виправлення проблеми з USDT/USDC парами
Перевіряє що система правильно вибирає USDT пари з DexScreener
"""

import logging
import sys

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Імпортуємо dex_client
from dex_client import dex_client

def test_quote_priority():
    """Тестує пріоритизацію USDT пар над USDC"""
    
    print("\n" + "="*80)
    print("🔧 ТЕСТ ВИПРАВЛЕННЯ: Пріоритизація USDT над USDC")
    print("="*80 + "\n")
    
    # Тестові символи
    test_symbols = ['BCH', 'ETH', 'BTC', 'SOL']
    
    for symbol in test_symbols:
        print(f"\n{'='*60}")
        print(f"📊 Тестуємо: {symbol}")
        print(f"{'='*60}")
        
        try:
            # Отримуємо найкращу пару
            pair_data = dex_client.resolve_best_pair(symbol)
            
            if pair_data:
                price = pair_data.get('price_usd', 0)
                liquidity = pair_data.get('liquidity_usd', 0)
                volume = pair_data.get('volume_24h', 0)
                quote_symbol = pair_data.get('quote_symbol', 'UNKNOWN')
                chain = pair_data.get('chain', 'unknown')
                dex = pair_data.get('dex_id', 'unknown')
                
                print(f"✅ Знайдено пару: {symbol}/{quote_symbol}")
                print(f"   💰 Ціна: ${price:.6f}")
                print(f"   💧 Ліквідність: ${liquidity:,.0f}")
                print(f"   📊 Обсяг 24г: ${volume:,.0f}")
                print(f"   ⛓️  Мережа: {chain}")
                print(f"   🏪 DEX: {dex}")
                
                # Перевірка чи це USDT пара
                if quote_symbol == 'USDT':
                    print(f"   ✅ ПРАВИЛЬНО: Вибрано USDT пару")
                elif quote_symbol == 'USDC':
                    print(f"   ⚠️  УВАГА: Вибрано USDC пару (можливо немає USDT пари з достатньою ліквідністю)")
                else:
                    print(f"   ℹ️  ІНФО: Вибрано {quote_symbol} пару")
            else:
                print(f"❌ Не вдалося знайти пару для {symbol}")
                
        except Exception as e:
            print(f"❌ Помилка при тестуванні {symbol}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("🏁 ТЕСТ ЗАВЕРШЕНО")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_quote_priority()
