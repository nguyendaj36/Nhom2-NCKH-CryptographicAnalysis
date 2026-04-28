import requests
import time
from tenacity import retry, wait_exponential, stop_after_attempt

class BaseBinanceAPI:
    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3"

    # Tự động thử lại tối đa 5 lần nếu rớt mạng, thời gian chờ tăng dần 2s, 4s, 8s...
    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
    def _send_request(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params, timeout=10)
        
        # Xử lý khi bị Binance chặn do quá nhiều request (HTTP 429)
        if response.status_code == 429:
            print("Chạm ngưỡng Rate Limit. Đang chờ để tiếp tục...")
            time.sleep(10)
            response.raise_for_status() # Ép retry
            
        response.raise_for_status()
        return response.json()