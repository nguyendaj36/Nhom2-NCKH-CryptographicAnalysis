import time
import schedule
import sys
from crypto.pipelines.historical_sync import sync_historical_data
from core.database import MongoDBClient

# 1. CẤU HÌNH HỆ THỐNG - 50 COINS
TARGET_COINS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", 
    "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "DOTUSDT", 
    "MATICUSDT", "SHIBUSDT", "LTCUSDT", "UNIUSDT", "NEARUSDT", 
    "APTUSDT", "OPUSDT", "ARBUSDT", "INJUSDT", "RNDRUSDT", 
    "FETUSDT", "GRTUSDT", "LDOUSDT", "ATOMUSDT", "ICPUSDT", 
    "FILUSDT", "VETUSDT", "STXUSDT", "TIAUSDT", "SUIUSDT", 
    "SEIUSDT", "GALAUSDT", "SANDUSDT", "MANAUSDT", "AXSUSDT", 
    "APEUSDT", "THETAUSDT", "EGLDUSDT", "FTMUSDT", "ALGOUSDT", 
    "QNTUSDT", "SNXUSDT", "CRVUSDT", "MKRUSDT", "AAVEUSDT", 
    "PEPEUSDT", "WLDUSDT", "DYDXUSDT", "ORDIUSDT", "GMXUSDT"
]
INTERVAL = "15m"  # Khung thời gian nến là 15 phút

def job_fetch_crypto():
    """Hàm này sẽ được gọi mỗi 15 phút"""
    print("\n" + "="*50)
    print(f"🚀 BẮT ĐẦU CẬP NHẬT 50 COINS LÚC: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    success_count = 0
    total_coins = len(TARGET_COINS)
    
    # Dùng enumerate để lấy số thứ tự (i) của từng đồng coin
    for i, symbol in enumerate(TARGET_COINS, 1):
        try:
            # Lấy 5 nến gần nhất, cơ chế Upsert sẽ chống trùng lặp
            sync_historical_data(symbol=symbol, interval=INTERVAL, limit=5)
            success_count += 1
        except Exception as e:
            # Xóa sạch dòng tiến độ hiện tại trước khi in lỗi để chữ không bị đè lên nhau
            print(f"\r{' '*70}\r", end="", flush=True)
            print(f"[!] Bỏ qua {symbol} do lỗi: {e}")
            
        # Nghỉ 1 giây giữa các coin để không bị Binance chặn IP
        time.sleep(1) 
        
        # --- LOGIC VẼ THANH TIẾN ĐỘ ---
        percent = i / total_coins
        bar_length = 30  # Độ dài của thanh tiến độ (30 ký tự)
        filled_length = int(bar_length * percent)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        # In đè lên dòng hiện tại: Hiển thị thanh bar, % hoàn thành, số coin và tên coin
        print(f"\r⏳ Đang tải: |{bar}| {percent:.0%} ({i}/{total_coins}) - {symbol:<8}", end="", flush=True)
        
    # In một dòng trống để ngắt khỏi thanh tiến độ sau khi hoàn thành 100%
    print("\n" + "-" * 50)
    print(f"✅ HOÀN THÀNH LƯỢT CẬP NHẬT! (Thành công {success_count}/{total_coins})")

if __name__ == "__main__":
    print("=== HỆ THỐNG AUTO-SYNC DỮ LIỆU LỚN ĐÃ KHỞI ĐỘNG ===")
    
    # Chạy ngay lập tức lần đầu tiên khi vừa khởi động tool
    job_fetch_crypto()
    
    # Lên lịch trình: Cứ mỗi 15 phút thì thực thi hàm job_fetch_crypto
    schedule.every(15).minutes.do(job_fetch_crypto)
    
    # Vòng lặp vô hạn để duy trì chương trình luôn bật và hiển thị đếm ngược
    try:
        while True:
            # Lấy số giây còn lại cho đến lần chạy tiếp theo
            idle_secs = schedule.idle_seconds()
            
            if idle_secs is not None and idle_secs > 0:
                # Tính toán phút và giây
                mins, secs = divmod(int(idle_secs), 60)
                timer_str = f"{mins:02d}:{secs:02d}"
                
                # In đè lên dòng hiện tại (dùng \r)
                print(f"\r⏳ Lấy dữ liệu mới sau: {timer_str}   ", end="", flush=True)
            else:
                # Xóa dòng đếm ngược khi bắt đầu chu kỳ mới để log in ra được sạch sẽ
                print("\r" + " " * 50 + "\r", end="", flush=True)
            
            schedule.run_pending()
            time.sleep(1) 
            
    except KeyboardInterrupt:
        print("\n\n[!] Đã tắt hệ thống Auto-Sync an toàn.")