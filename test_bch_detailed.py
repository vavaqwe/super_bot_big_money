#!/usr/bin/env python3
"""
Детальний аналіз BCH пар на DexScreener
"""

import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(message)s')

def analyze_bch_pairs():
    """Аналізує всі доступні пари BCH на DexScreener"""
    
    print("\n" + "="*80)
    print("🔍 ДЕТАЛЬНИЙ АНАЛІЗ BCH ПАР")
    print("="*80 + "\n")
    
    # Виконуємо запит до DexScreener API
    url = "https://api.dexscreener.com/latest/dex/search/?q=BCH"
    
    try:
        response = requests.get(url, timeout=20)
        data = response.json()
        
        if not data or not data.get('pairs'):
            print("❌ Не знайдено пар для BCH")
            return
        
        # Фільтруємо пари
        all_pairs = data['pairs']
        
        # Розділяємо пари по типу
        usdt_pairs = []
        usdc_pairs = []
        other_pairs = []
        
        print(f"📊 Всього знайдено пар: {len(all_pairs)}\n")
        
        for pair in all_pairs[:30]:  # Аналізуємо перші 30 пар
            base = pair.get('baseToken', {}).get('symbol', '').upper()
            quote = pair.get('quoteToken', {}).get('symbol', '').upper()
            
            # Пропускаємо пари де BCH не base токен
            if base != 'BCH':
                continue
            
            liquidity = float(pair.get('liquidity', {}).get('usd', 0))
            volume = float(pair.get('volume', {}).get('h24', 0))
            price = float(pair.get('priceUsd', 0))
            chain = pair.get('chainId', 'unknown')
            dex = pair.get('dexId', 'unknown')
            
            pair_info = {
                'base': base,
                'quote': quote,
                'price': price,
                'liquidity': liquidity,
                'volume': volume,
                'chain': chain,
                'dex': dex
            }
            
            if quote == 'USDT':
                usdt_pairs.append(pair_info)
            elif quote == 'USDC':
                usdc_pairs.append(pair_info)
            else:
                other_pairs.append(pair_info)
        
        # Виводимо результати
        print("🟢 BCH/USDT ПАРИ:")
        print("-" * 80)
        if usdt_pairs:
            for i, p in enumerate(sorted(usdt_pairs, key=lambda x: x['liquidity'], reverse=True), 1):
                print(f"{i}. {p['base']}/{p['quote']} на {p['chain']} ({p['dex']})")
                print(f"   💰 Ціна: ${p['price']:.2f}")
                print(f"   💧 Ліквідність: ${p['liquidity']:,.0f}")
                print(f"   📊 Обсяг 24г: ${p['volume']:,.0f}")
                print()
        else:
            print("   ❌ Немає BCH/USDT пар\n")
        
        print("🔵 BCH/USDC ПАРИ:")
        print("-" * 80)
        if usdc_pairs:
            for i, p in enumerate(sorted(usdc_pairs, key=lambda x: x['liquidity'], reverse=True), 1):
                print(f"{i}. {p['base']}/{p['quote']} на {p['chain']} ({p['dex']})")
                print(f"   💰 Ціна: ${p['price']:.2f}")
                print(f"   💧 Ліквідність: ${p['liquidity']:,.0f}")
                print(f"   📊 Обсяг 24г: ${p['volume']:,.0f}")
                print()
        else:
            print("   ❌ Немає BCH/USDC пар\n")
        
        print("⚪ ІНШІ BCH ПАРИ (топ 5 за ліквідністю):")
        print("-" * 80)
        if other_pairs:
            for i, p in enumerate(sorted(other_pairs, key=lambda x: x['liquidity'], reverse=True)[:5], 1):
                print(f"{i}. {p['base']}/{p['quote']} на {p['chain']} ({p['dex']})")
                print(f"   💰 Ціна: ${p['price']:.2f}")
                print(f"   💧 Ліквідність: ${p['liquidity']:,.0f}")
                print(f"   📊 Обсяг 24г: ${p['volume']:,.0f}")
                print()
        else:
            print("   ❌ Немає інших BCH пар\n")
        
        print("="*80)
        print("📊 СТАТИСТИКА:")
        print(f"   USDT пар: {len(usdt_pairs)}")
        print(f"   USDC пар: {len(usdc_pairs)}")
        print(f"   Інших пар: {len(other_pairs)}")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"❌ Помилка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_bch_pairs()
