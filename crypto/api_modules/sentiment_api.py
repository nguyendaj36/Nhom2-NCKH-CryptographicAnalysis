import pandas as pd
from crypto.api_modules.base_api import BaseBinanceAPI

class SentimentAPI(BaseBinanceAPI):
    def __init__(self):
        super().__init__()
        # Ghi đè URL sang máy chủ Futures Data của Binance
        self.base_url = "https://fapi.binance.com"

    def get_long_short_ratio(self, symbol, period="15m", limit=30):
        """Lấy Tỷ lệ Long/Short của toàn bộ tài khoản (Global Long/Short Ratio)"""
        endpoint = "futures/data/globalLongShortAccountRatio"
        params = {
            'symbol': symbol,
            'period': period,
            'limit': limit
        }
        
        try:
            data = self._send_request(endpoint, params)
            if not data:
                return None
                
            df = pd.DataFrame(data)
            # Chuyển đổi timestamp sang DateTime
            df['Open_time'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Ép kiểu dữ liệu sang số thực
            df['longShortRatio'] = df['longShortRatio'].astype(float)
            df['longAccount'] = df['longAccount'].astype(float)
            df['shortAccount'] = df['shortAccount'].astype(float)
            
            # Trả về: Thời gian, Tỷ lệ L/S, % Tài khoản Long, % Tài khoản Short
            return df[['Open_time', 'longShortRatio', 'longAccount', 'shortAccount']]
            
        except Exception as e:
            # Bỏ qua lỗi nếu đồng coin đó không có giao dịch Futures trên Binance
            return None