import pandas as pd
from crypto.api_modules.base_api import BaseBinanceAPI

class KlinesAPI(BaseBinanceAPI):
    def get_historical_klines(self, symbol, interval, limit=1000):
        """Lấy dữ liệu OHLCV lịch sử và Lực Cung - Cầu"""
        endpoint = "klines"
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        
        # Gọi hàm _send_request từ class cha (BaseBinanceAPI)
        data = self._send_request(endpoint, params)
        
        columns = ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume',
                   'Close_time', 'Quote_asset_volume', 'Number_of_trades',
                   'Taker_buy_base_volume', 'Taker_buy_quote_volume', 'Ignore']
        df = pd.DataFrame(data, columns=columns)
        df['Open_time'] = pd.to_datetime(df['Open_time'], unit='ms')
        
        # Chuyển đổi kiểu dữ liệu số để Pandas dễ dàng xử lý
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 
                        'Number_of_trades', 'Taker_buy_base_volume', 'Taker_buy_quote_volume']
        df[numeric_cols] = df[numeric_cols].astype(float)
        
        # Trả về DataFrame chứa các cột quan trọng nhất
        return df[['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 
                   'Number_of_trades', 'Taker_buy_base_volume', 'Taker_buy_quote_volume']]