from crypto.api_modules.klines_api import KlinesAPI
from crypto.api_modules.sentiment_api import SentimentAPI
from core.database import MongoDBClient
from pymongo import UpdateOne

def sync_historical_data(symbol, interval, limit=5):
    # Khởi tạo các module kết nối
    api_kline = KlinesAPI()
    api_sentiment = SentimentAPI()
    db_client = MongoDBClient()
    
    # Tạo 2 bảng (collection) tách biệt để không bị lộn xộn dữ liệu
    col_kline = db_client.get_collection(f"crypto_{symbol}_{interval}_klines")
    col_longshort = db_client.get_collection(f"crypto_{symbol}_{interval}_longshort")
    
    try:
        # --- 1. ĐỒNG BỘ DỮ LIỆU NẾN & LỰC MUA CHỦ ĐỘNG ---
        df_kline = api_kline.get_historical_klines(symbol, interval, limit)
        if df_kline is not None and not df_kline.empty:
            records_kline = df_kline.to_dict(orient='records')
            ops_kline = [
                UpdateOne({'Open_time': r['Open_time']}, {'$set': r}, upsert=True)
                for r in records_kline
            ]
            # Thực thi đẩy dữ liệu vào MongoDB
            res_kline = col_kline.bulk_write(ops_kline)
            # In log rút gọn để không quá dài
            # print(f"[+] {symbol} (Klines): Cập nhật {res_kline.upserted_count + res_kline.modified_count} bản ghi.")
        
        # --- 2. ĐỒNG BỘ DỮ LIỆU TÂM LÝ LONG/SHORT ---
        df_ls = api_sentiment.get_long_short_ratio(symbol, period=interval, limit=limit)
        if df_ls is not None and not df_ls.empty:
            records_ls = df_ls.to_dict(orient='records')
            ops_ls = [
                UpdateOne({'Open_time': r['Open_time']}, {'$set': r}, upsert=True)
                for r in records_ls
            ]
            # Thực thi đẩy dữ liệu vào MongoDB
            res_ls = col_longshort.bulk_write(ops_ls)
            
    except Exception as e:
        print(f"[!] Lỗi khi đồng bộ {symbol}: {e}")