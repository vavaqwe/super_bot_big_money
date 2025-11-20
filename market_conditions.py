# """
# 🔍 Модуль відстеження ринкових умов для автоматичного переключення режимів
# Моніторить RSI BTC, Fear & Greed Index, та зміну ціни BTC
# Створено для Trinkenbot - Automatic Trading Mode Switching
# """

# import requests
# import logging
# import time
# from typing import Dict, Optional, Tuple
# from datetime import datetime, timedelta
# import numpy as np

# logger = logging.getLogger(__name__)

# class MarketConditionsMonitor:
#     """Моніторинг ринкових умов для автоматичного переключення режимів"""
    
#     def __init__(self):
#         self.cache = {}
#         self.cache_ttl = 60  # Кешування на 1 хвилину
#         self.btc_price_history = []  # Історія цін BTC для розрахунку зміни
#         self.max_history_size = 100  # Зберігаємо останні 100 записів
        
#     def _get_cached_data(self, key: str) -> Optional[any]:
#         """Отримати дані з кешу"""
#         if key in self.cache:
#             timestamp, data = self.cache[key]
#             if time.time() - timestamp < self.cache_ttl:
#                 return data
#         return None
    
#     def _cache_data(self, key: str, data: any):
#         """Зберегти дані в кеш"""
#         self.cache[key] = (time.time(), data)
    
#     def get_btc_rsi(self, period: int = 14) -> Optional[float]:
#         """
#         Отримує RSI для BTC
#         Використовує дані з Binance або іншої біржі
#         """
#         try:
#             # Перевіряємо кеш
#             cached = self._get_cached_data('btc_rsi')
#             if cached is not None:
#                 return cached
            
#             # Отримуємо історичні дані BTC з Binance
#             url = "https://api.binance.com/api/v3/klines"
#             params = {
#                 'symbol': 'BTCUSDT',
#                 'interval': '1h',  # 1-годинні свічки
#                 'limit': period + 1  # Потрібно period+1 для розрахунку RSI
#             }
            
#             response = requests.get(url, params=params, timeout=10)
#             if response.status_code != 200:
#                 logger.warning(f"⚠️ Помилка отримання даних BTC: {response.status_code}")
#                 return None
            
#             klines = response.json()
            
#             # Витягуємо ціни закриття
#             closes = [float(kline[4]) for kline in klines]
            
#             if len(closes) < period + 1:
#                 logger.warning(f"⚠️ Недостатньо даних для RSI: {len(closes)} < {period + 1}")
#                 return None
            
#             # Розраховуємо RSI
#             rsi = self._calculate_rsi(closes, period)
            
#             # Кешуємо результат
#             self._cache_data('btc_rsi', rsi)
            
#             logger.info(f"📊 BTC RSI({period}): {rsi:.2f}")
#             return rsi
            
#         except Exception as e:
#             logger.error(f"❌ Помилка розрахунку BTC RSI: {e}")
#             return None
    
#     def _calculate_rsi(self, prices: list, period: int = 14) -> float:
#         """Розрахунок RSI вручну"""
#         if len(prices) < period + 1:
#             return 50.0  # Нейтральне значення
        
#         deltas = np.diff(prices)
#         gains = np.where(deltas > 0, deltas, 0)
#         losses = np.where(deltas < 0, -deltas, 0)
        
#         avg_gain = np.mean(gains[-period:])
#         avg_loss = np.mean(losses[-period:])
        
#         if avg_loss == 0:
#             return 100.0
        
#         rs = avg_gain / avg_loss
#         rsi = 100 - (100 / (1 + rs))
#         return float(rsi)
    
#     def get_fear_greed_index(self) -> Optional[int]:
#         """
#         Отримує Fear & Greed Index з офіційного API
#         Повертає значення від 0 (Extreme Fear) до 100 (Extreme Greed)
#         """
#         try:
#             # Перевіряємо кеш
#             cached = self._get_cached_data('fear_greed')
#             if cached is not None:
#                 return cached
            
#             # API Fear & Greed Index
#             url = "https://api.alternative.me/fng/"
#             params = {'limit': 1}  # Отримуємо тільки останнє значення
            
#             response = requests.get(url, params=params, timeout=10)
#             if response.status_code != 200:
#                 logger.warning(f"⚠️ Помилка отримання Fear & Greed Index: {response.status_code}")
#                 return None
            
#             data = response.json()
            
#             if 'data' not in data or len(data['data']) == 0:
#                 logger.warning("⚠️ Немає даних Fear & Greed Index")
#                 return None
            
#             fear_greed_value = int(data['data'][0]['value'])
#             fear_greed_classification = data['data'][0]['value_classification']
            
#             # Кешуємо результат
#             self._cache_data('fear_greed', fear_greed_value)
            
#             logger.info(f"😱 Fear & Greed Index: {fear_greed_value} ({fear_greed_classification})")
#             return fear_greed_value
            
#         except Exception as e:
#             logger.error(f"❌ Помилка отримання Fear & Greed Index: {e}")
#             return None
    
#     def get_btc_price_change_1h(self) -> Optional[float]:
#         """
#         Розраховує зміну ціни BTC за останню годину (у %)
#         Позитивне значення = зростання, негативне = падіння
#         """
#         try:
#             # Перевіряємо кеш
#             cached = self._get_cached_data('btc_1h_change')
#             if cached is not None:
#                 return cached
            
#             # Отримуємо поточну ціну та ціну годину тому
#             url = "https://api.binance.com/api/v3/klines"
#             params = {
#                 'symbol': 'BTCUSDT',
#                 'interval': '1h',
#                 'limit': 2  # Поточна година + попередня
#             }
            
#             response = requests.get(url, params=params, timeout=10)
#             if response.status_code != 200:
#                 logger.warning(f"⚠️ Помилка отримання даних BTC: {response.status_code}")
#                 return None
            
#             klines = response.json()
            
#             if len(klines) < 2:
#                 logger.warning("⚠️ Недостатньо даних для розрахунку зміни ціни")
#                 return None
            
#             # Ціна годину тому (закриття попередньої свічки)
#             price_1h_ago = float(klines[0][4])
#             # Поточна ціна (закриття поточної свічки)
#             current_price = float(klines[1][4])
            
#             # Розраховуємо зміну у відсотках
#             price_change_pct = ((current_price - price_1h_ago) / price_1h_ago) * 100
            
#             # Зберігаємо в історію
#             self.btc_price_history.append({
#                 'timestamp': time.time(),
#                 'price': current_price,
#                 'change_1h': price_change_pct
#             })
            
#             # Обмежуємо розмір історії
#             if len(self.btc_price_history) > self.max_history_size:
#                 self.btc_price_history = self.btc_price_history[-self.max_history_size:]
            
#             # Кешуємо результат
#             self._cache_data('btc_1h_change', price_change_pct)
            
#             logger.info(f"💰 BTC зміна за 1 годину: {price_change_pct:+.2f}% (${price_1h_ago:.2f} → ${current_price:.2f})")
#             return price_change_pct
            
#         except Exception as e:
#             logger.error(f"❌ Помилка розрахунку зміни ціни BTC: {e}")
#             return None
    
#     def check_all_conditions(self) -> Dict[str, any]:
#         """
#         Перевіряє всі ринкові умови
#         Повертає словник з усіма показниками
#         """
#         try:
#             conditions = {
#                 'btc_rsi': self.get_btc_rsi(),
#                 'fear_greed': self.get_fear_greed_index(),
#                 'btc_1h_change': self.get_btc_price_change_1h(),
#                 'timestamp': datetime.now().isoformat()
#             }
            
#             # Форматуємо тільки якщо значення не None
#             rsi_str = f"{conditions['btc_rsi']:.2f}" if conditions['btc_rsi'] is not None else "N/A"
#             fg_str = f"{conditions['fear_greed']}" if conditions['fear_greed'] is not None else "N/A"
#             btc_str = f"{conditions['btc_1h_change']:+.2f}%" if conditions['btc_1h_change'] is not None else "N/A"
            
#             logger.info(f"📊 Ринкові умови: RSI={rsi_str}, F&G={fg_str}, BTC 1h={btc_str}")
            
#             return conditions
            
#         except Exception as e:
#             logger.error(f"❌ Помилка перевірки ринкових умов: {e}")
#             return {
#                 'btc_rsi': None,
#                 'fear_greed': None,
#                 'btc_1h_change': None,
#                 'timestamp': datetime.now().isoformat()
#             }

#     def should_switch_to_bull(self, rsi_threshold, fear_greed_threshold, btc_growth_threshold, btc_price_threshold):
#         """
#         Перевіряє чи варто перемикатись в BULL режим
#         Умови (OR):
#         1. BTC ціна вище порогу (напр. 100k)
#         2. RSI вище порогу (напр. 50)
#         3. Fear & Greed вище порогу (напр. 45)
#         4. BTC ріст за годину вище порогу (напр. 3%)
#         """
#         try:
#             reasons = []
            
#             # 1. Перевірка ціни BTC
#             btc_data = self.get_btc_data()
#             if btc_data:
#                 current_price = btc_data.get('price', 0)
#                 growth = btc_data.get('growth_1h', 0)
                
#                 # Перевірка абсолютної ціни
#                 if current_price > btc_price_threshold:
#                     logging.info(f"🐂 BULL SIGNAL: BTC Price ${current_price} > ${btc_price_threshold}")
#                     return True, f"BTC Price break: ${current_price:.0f} > ${btc_price_threshold}"

#                 # Перевірка росту
#                 if growth > btc_growth_threshold:
#                     logging.info(f"🐂 BULL SIGNAL: BTC Growth {growth:.2f}% > {btc_growth_threshold}%")
#                     return True, f"BTC Pump: +{growth:.2f}% in 1h"
            
#             # 2. Перевірка Fear & Greed
#             fg_index = self.get_fear_and_greed_index()
#             if fg_index and fg_index > fear_greed_threshold:
#                 logging.info(f"🐂 BULL SIGNAL: Fear&Greed {fg_index} > {fear_greed_threshold}")
#                 return True, f"Sentiment improved: F&G {fg_index}"
                
#             # 3. Перевірка RSI (через біткоїн або загальний ринок)
#             # Тут можна додати логіку RSI, якщо у вас є джерело
#             # поки що повертаємо False якщо інші умови не спрацювали
            
#             return False, ""
            
#         except Exception as e:
#             logging.error(f"Error in bull check: {e}")
#             return False, ""

#     def should_switch_to_conservative(self, rsi_threshold, fear_greed_threshold, btc_decline_threshold, btc_price_threshold):
#         """
#         Перевіряє чи варто перемикатись в CONSERVATIVE режим
#         Умови (OR):
#         1. BTC ціна нижче порогу (напр. 98k)
#         2. RSI нижче порогу (напр. 45)
#         3. Fear & Greed нижче порогу (напр. 35)
#         4. BTC падіння за годину більше порогу (напр. -2%)
#         """
#         try:
#             # 1. Перевірка ціни BTC
#             btc_data = self.get_btc_data()
#             if btc_data:
#                 current_price = btc_data.get('price', 0)
#                 growth = btc_data.get('growth_1h', 0)
                
#                 # Перевірка абсолютної ціни
#                 if current_price > 0 and current_price < btc_price_threshold:
#                     logging.info(f"🛡️ CONSERVATIVE SIGNAL: BTC Price ${current_price} < ${btc_price_threshold}")
#                     return True, f"BTC Price drop: ${current_price:.0f} < ${btc_price_threshold}"

#                 # Перевірка падіння (наприклад growth < -2.0)
#                 if growth < btc_decline_threshold:
#                     logging.info(f"🛡️ CONSERVATIVE SIGNAL: BTC Dump {growth:.2f}% < {btc_decline_threshold}%")
#                     return True, f"BTC Dump: {growth:.2f}% in 1h"
            
#             # 2. Перевірка Fear & Greed
#             fg_index = self.get_fear_and_greed_index()
#             if fg_index and fg_index < fear_greed_threshold:
#                 logging.info(f"🛡️ CONSERVATIVE SIGNAL: Fear&Greed {fg_index} < {fear_greed_threshold}")
#                 return True, f"Market Fear: F&G {fg_index}"
            
#             return False, ""
            
#         except Exception as e:
#             logging.error(f"Error in conservative check: {e}")
#             return False, ""
    
#     # def should_switch_to_bull(self, rsi_threshold: float, fg_threshold: int, btc_growth_threshold: float) -> Tuple[bool, str]:
#     #     """
#     #     Перевіряє чи потрібно переключитися на BULL режим
#     #     Повертає (True/False, причина)
#     #     """
#     #     try:
#     #         conditions = self.check_all_conditions()
            
#     #         # Перевіряємо чи всі дані доступні
#     #         if None in [conditions['btc_rsi'], conditions['fear_greed'], conditions['btc_1h_change']]:
#     #             return False, "Недостатньо даних для прийняття рішення"
            
#     #         rsi = conditions['btc_rsi']
#     #         fg = conditions['fear_greed']
#     #         btc_change = conditions['btc_1h_change']
            
#     #         # Перевіряємо всі умови для переходу в BULL
#     #         rsi_ok = rsi > rsi_threshold
#     #         fg_ok = fg > fg_threshold
#     #         btc_ok = btc_change > btc_growth_threshold
            
#     #         if rsi_ok and fg_ok and btc_ok:
#     #             reason = (f"✅ BULL умови виконано: RSI={rsi:.1f}>{rsi_threshold}, "
#     #                      f"F&G={fg}>{fg_threshold}, BTC={btc_change:+.2f}%>{btc_growth_threshold}%")
#     #             return True, reason
            
#     #         # Якщо не всі умови виконані
#     #         reasons = []
#     #         if not rsi_ok:
#     #             reasons.append(f"RSI={rsi:.1f}<={rsi_threshold}")
#     #         if not fg_ok:
#     #             reasons.append(f"F&G={fg}<={fg_threshold}")
#     #         if not btc_ok:
#     #             reasons.append(f"BTC={btc_change:+.2f}%<={btc_growth_threshold}%")
            
#     #         return False, f"❌ BULL умови не виконано: {', '.join(reasons)}"
            
#     #     except Exception as e:
#     #         logger.error(f"❌ Помилка перевірки умов переходу в BULL: {e}")
#     #         return False, f"Помилка: {str(e)}"
    
#     # def should_switch_to_conservative(self, rsi_threshold: float, fg_threshold: int, btc_decline_threshold: float) -> Tuple[bool, str]:
#     #     """
#     #     Перевіряє чи потрібно переключитися на CONSERVATIVE режим
#     #     Повертає (True/False, причина)
#     #     """
#     #     try:
#     #         conditions = self.check_all_conditions()
            
#     #         # Перевіряємо чи всі дані доступні
#     #         if None in [conditions['btc_rsi'], conditions['fear_greed'], conditions['btc_1h_change']]:
#     #             return False, "Недостатньо даних для прийняття рішення"
            
#     #         rsi = conditions['btc_rsi']
#     #         fg = conditions['fear_greed']
#     #         btc_change = conditions['btc_1h_change']
            
#     #         # Перевіряємо всі умови для переходу в CONSERVATIVE
#     #         rsi_ok = rsi < rsi_threshold
#     #         fg_ok = fg < fg_threshold
#     #         btc_ok = btc_change < btc_decline_threshold
            
#     #         if rsi_ok and fg_ok and btc_ok:
#     #             reason = (f"✅ CONSERVATIVE умови виконано: RSI={rsi:.1f}<{rsi_threshold}, "
#     #                      f"F&G={fg}<{fg_threshold}, BTC={btc_change:+.2f}%<{btc_decline_threshold}%")
#     #             return True, reason
            
#     #         # Якщо не всі умови виконані
#     #         reasons = []
#     #         if not rsi_ok:
#     #             reasons.append(f"RSI={rsi:.1f}>={rsi_threshold}")
#     #         if not fg_ok:
#     #             reasons.append(f"F&G={fg}>={fg_threshold}")
#     #         if not btc_ok:
#     #             reasons.append(f"BTC={btc_change:+.2f}%>={btc_decline_threshold}%")
            
#     #         return False, f"❌ CONSERVATIVE умови не виконано: {', '.join(reasons)}"
            
#     #     except Exception as e:
#     #         logger.error(f"❌ Помилка перевірки умов переходу в CONSERVATIVE: {e}")
#     #         return False, f"Помилка: {str(e)}"


# # Глобальний екземпляр монітора
# market_monitor = MarketConditionsMonitor()


"""
🔍 Модуль відстеження ринкових умов для автоматичного переключення режимів
Моніторить RSI BTC, Fear & Greed Index, та зміну ціни BTC
Створено для Trinkenbot - Automatic Trading Mode Switching
"""

import requests
import logging
import time
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np

logger = logging.getLogger(__name__)

class MarketConditionsMonitor:
    """Моніторинг ринкових умов для автоматичного переключення режимів"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 60  # Кешування на 1 хвилину
        self.btc_price_history = []  # Історія цін BTC для розрахунку зміни
        self.max_history_size = 100  # Зберігаємо останні 100 записів
        
    def _get_cached_data(self, key: str) -> Optional[any]:
        """Отримати дані з кешу"""
        if key in self.cache:
            timestamp, data = self.cache[key]
            if time.time() - timestamp < self.cache_ttl:
                return data
        return None
    
    def _cache_data(self, key: str, data: any):
        """Зберегти дані в кеш"""
        self.cache[key] = (time.time(), data)
    
    def get_btc_rsi(self, period: int = 14) -> Optional[float]:
        """
        Отримує RSI для BTC
        Використовує дані з Binance або іншої біржі
        """
        try:
            # Перевіряємо кеш
            cached = self._get_cached_data('btc_rsi')
            if cached is not None:
                return cached
            
            # Отримуємо історичні дані BTC з Binance
            url = "https://api.binance.com/api/v3/klines"
            params = {
                'symbol': 'BTCUSDT',
                'interval': '1h',  # 1-годинні свічки
                'limit': period + 1  # Потрібно period+1 для розрахунку RSI
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                logger.warning(f"⚠️ Помилка отримання даних BTC: {response.status_code}")
                return None
            
            klines = response.json()
            
            # Витягуємо ціни закриття
            closes = [float(kline[4]) for kline in klines]
            
            if len(closes) < period + 1:
                logger.warning(f"⚠️ Недостатньо даних для RSI: {len(closes)} < {period + 1}")
                return None
            
            # Розраховуємо RSI
            rsi = self._calculate_rsi(closes, period)
            
            # Кешуємо результат
            self._cache_data('btc_rsi', rsi)
            
            logger.info(f"📊 BTC RSI({period}): {rsi:.2f}")
            return rsi
            
        except Exception as e:
            logger.error(f"❌ Помилка розрахунку BTC RSI: {e}")
            return None
    
    def _calculate_rsi(self, prices: list, period: int = 14) -> float:
        """Розрахунок RSI вручну"""
        if len(prices) < period + 1:
            return 50.0  # Нейтральне значення
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return float(rsi)
    
    def get_fear_greed_index(self) -> Optional[int]:
        """
        Отримує Fear & Greed Index з офіційного API
        Повертає значення від 0 (Extreme Fear) до 100 (Extreme Greed)
        """
        try:
            # Перевіряємо кеш
            cached = self._get_cached_data('fear_greed')
            if cached is not None:
                return cached
            
            # API Fear & Greed Index
            url = "https://api.alternative.me/fng/"
            params = {'limit': 1}  # Отримуємо тільки останнє значення
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                logger.warning(f"⚠️ Помилка отримання Fear & Greed Index: {response.status_code}")
                return None
            
            data = response.json()
            
            if 'data' not in data or len(data['data']) == 0:
                logger.warning("⚠️ Немає даних Fear & Greed Index")
                return None
            
            fear_greed_value = int(data['data'][0]['value'])
            fear_greed_classification = data['data'][0]['value_classification']
            
            # Кешуємо результат
            self._cache_data('fear_greed', fear_greed_value)
            
            logger.info(f"😱 Fear & Greed Index: {fear_greed_value} ({fear_greed_classification})")
            return fear_greed_value
            
        except Exception as e:
            logger.error(f"❌ Помилка отримання Fear & Greed Index: {e}")
            return None
    
    def get_btc_price_change_1h(self) -> Optional[float]:
        """
        Розраховує зміну ціни BTC за останню годину (у %)
        Позитивне значення = зростання, негативне = падіння
        """
        try:
            # Перевіряємо кеш
            cached = self._get_cached_data('btc_1h_change')
            if cached is not None:
                return cached
            
            # Отримуємо поточну ціну та ціну годину тому
            url = "https://api.binance.com/api/v3/klines"
            params = {
                'symbol': 'BTCUSDT',
                'interval': '1h',
                'limit': 2  # Поточна година + попередня
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                logger.warning(f"⚠️ Помилка отримання даних BTC: {response.status_code}")
                return None
            
            klines = response.json()
            
            if len(klines) < 2:
                logger.warning("⚠️ Недостатньо даних для розрахунку зміни ціни")
                return None
            
            # Ціна годину тому (закриття попередньої свічки)
            price_1h_ago = float(klines[0][4])
            # Поточна ціна (закриття поточної свічки)
            current_price = float(klines[1][4])
            
            # Розраховуємо зміну у відсотках
            price_change_pct = ((current_price - price_1h_ago) / price_1h_ago) * 100
            
            # Зберігаємо в історію
            self.btc_price_history.append({
                'timestamp': time.time(),
                'price': current_price,
                'change_1h': price_change_pct
            })
            
            # Обмежуємо розмір історії
            if len(self.btc_price_history) > self.max_history_size:
                self.btc_price_history = self.btc_price_history[-self.max_history_size:]
            
            # Кешуємо результат
            self._cache_data('btc_1h_change', price_change_pct)
            
            logger.info(f"💰 BTC зміна за 1 годину: {price_change_pct:+.2f}% (${price_1h_ago:.2f} → ${current_price:.2f})")
            return price_change_pct
            
        except Exception as e:
            logger.error(f"❌ Помилка розрахунку зміни ціни BTC: {e}")
            return None

    # 🔥 [NEW] Додана функція, якої не вистачало
    def get_btc_data(self) -> Optional[Dict]:
        """
        Отримує повні дані по BTC (ціна та зміна)
        Використовується для логіки переключення режимів
        """
        try:
            # Використовуємо вже існуючі методи для отримання даних
            change_1h = self.get_btc_price_change_1h()
            
            # Отримуємо актуальну ціну (якщо get_btc_price_change_1h спрацював, у нас є кеш або історія)
            current_price = 0
            if self.btc_price_history:
                current_price = self.btc_price_history[-1]['price']
            else:
                 # Fallback: запит ціни якщо історії немає
                url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
                resp = requests.get(url, timeout=5).json()
                current_price = float(resp['price'])

            return {
                'price': current_price,
                'growth_1h': change_1h if change_1h is not None else 0.0
            }
        except Exception as e:
            logger.error(f"❌ Помилка get_btc_data: {e}")
            return None

    def check_all_conditions(self) -> Dict[str, any]:
        """
        Перевіряє всі ринкові умови
        Повертає словник з усіма показниками
        """
        try:
            conditions = {
                'btc_rsi': self.get_btc_rsi(),
                'fear_greed': self.get_fear_greed_index(),
                'btc_1h_change': self.get_btc_price_change_1h(),
                'timestamp': datetime.now().isoformat()
            }
            
            # Форматуємо тільки якщо значення не None
            rsi_str = f"{conditions['btc_rsi']:.2f}" if conditions['btc_rsi'] is not None else "N/A"
            fg_str = f"{conditions['fear_greed']}" if conditions['fear_greed'] is not None else "N/A"
            btc_str = f"{conditions['btc_1h_change']:+.2f}%" if conditions['btc_1h_change'] is not None else "N/A"
            
            logger.info(f"📊 Ринкові умови: RSI={rsi_str}, F&G={fg_str}, BTC 1h={btc_str}")
            
            return conditions
            
        except Exception as e:
            logger.error(f"❌ Помилка перевірки ринкових умов: {e}")
            return {
                'btc_rsi': None,
                'fear_greed': None,
                'btc_1h_change': None,
                'timestamp': datetime.now().isoformat()
            }

    def should_switch_to_bull(self, rsi_threshold, fear_greed_threshold, btc_growth_threshold, btc_price_threshold):
        """
        Перевіряє чи варто перемикатись в BULL режим
        """
        try:
            reasons = []
            
            # 1. Перевірка ціни BTC
            btc_data = self.get_btc_data() # ✅ ТЕПЕР ЦЕ ПРАЦЮВАТИМЕ
            if btc_data:
                current_price = btc_data.get('price', 0)
                growth = btc_data.get('growth_1h', 0)
                
                # Перевірка абсолютної ціни
                if current_price > btc_price_threshold:
                    logging.info(f"🐂 BULL SIGNAL: BTC Price ${current_price} > ${btc_price_threshold}")
                    return True, f"BTC Price break: ${current_price:.0f} > ${btc_price_threshold}"

                # Перевірка росту
                if growth > btc_growth_threshold:
                    logging.info(f"🐂 BULL SIGNAL: BTC Growth {growth:.2f}% > {btc_growth_threshold}%")
                    return True, f"BTC Pump: +{growth:.2f}% in 1h"
            
            # 2. Перевірка Fear & Greed (ВИПРАВЛЕНО НАЗВУ ФУНКЦІЇ)
            fg_index = self.get_fear_greed_index() # ✅ БУЛО get_fear_and_greed_index
            if fg_index and fg_index > fear_greed_threshold:
                logging.info(f"🐂 BULL SIGNAL: Fear&Greed {fg_index} > {fear_greed_threshold}")
                return True, f"Sentiment improved: F&G {fg_index}"
            
            return False, ""
            
        except Exception as e:
            logging.error(f"Error in bull check: {e}")
            return False, ""

    def should_switch_to_conservative(self, rsi_threshold, fear_greed_threshold, btc_decline_threshold, btc_price_threshold):
        """
        Перевіряє чи варто перемикатись в CONSERVATIVE режим
        """
        try:
            # 1. Перевірка ціни BTC
            btc_data = self.get_btc_data() # ✅ ТЕПЕР ЦЕ ПРАЦЮВАТИМЕ
            if btc_data:
                current_price = btc_data.get('price', 0)
                growth = btc_data.get('growth_1h', 0)
                
                # Перевірка абсолютної ціни
                if current_price > 0 and current_price < btc_price_threshold:
                    logging.info(f"🛡️ CONSERVATIVE SIGNAL: BTC Price ${current_price} < ${btc_price_threshold}")
                    return True, f"BTC Price drop: ${current_price:.0f} < ${btc_price_threshold}"

                # Перевірка падіння (наприклад growth < -2.0)
                if growth < btc_decline_threshold:
                    logging.info(f"🛡️ CONSERVATIVE SIGNAL: BTC Dump {growth:.2f}% < {btc_decline_threshold}%")
                    return True, f"BTC Dump: {growth:.2f}% in 1h"
            
            # 2. Перевірка Fear & Greed (ВИПРАВЛЕНО НАЗВУ ФУНКЦІЇ)
            fg_index = self.get_fear_greed_index() # ✅ БУЛО get_fear_and_greed_index
            if fg_index and fg_index < fear_greed_threshold:
                logging.info(f"🛡️ CONSERVATIVE SIGNAL: Fear&Greed {fg_index} < {fear_greed_threshold}")
                return True, f"Market Fear: F&G {fg_index}"
            
            return False, ""
            
        except Exception as e:
            logging.error(f"Error in conservative check: {e}")
            return False, ""


# Глобальний екземпляр монітора
market_monitor = MarketConditionsMonitor()