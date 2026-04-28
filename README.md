# 🚀 NCKH - Cryptographic & Stock Price Analysis System

## 📌 Overview
Hệ thống thu thập, xử lý và dự báo giá **cổ phiếu** và **tiền mã hóa** bằng các phương pháp **Machine Learning / Deep Learning**, được phát triển theo quy trình **Agile**.

Dự án xây dựng pipeline hoàn chỉnh:
**Data → Processing → Modeling → API → Deployment**

---

## 🎯 Objectives
- Crawl dữ liệu từ:
  - Binance (crypto)
  - VNStock / API tài chính
- Xây dựng pipeline xử lý dữ liệu (ETL)
- Phân tích & trực quan hóa dữ liệu
- Áp dụng ML/DL để dự đoán:
  - XGBoost
  - LSTM
- Xây dựng RESTful API
- Triển khai thực tế

---

## 🧱 System Architecture


Data Sources
↓
Crawler / API
↓
Data Processing
↓
Database
↓
ML/DL Models
↓
Backend API
↓
Dashboard / Client


---

## 🛠️ Technologies

### 🔹 Programming Language
- Python 3.x

### 🔹 Machine Learning / Deep Learning
- Scikit-learn
- XGBoost
- TensorFlow / PyTorch

### 🔹 Data Processing
- Pandas
- NumPy

### 🔹 Database
- PostgreSQL / MySQL
- MongoDB

### 🔹 Data Collection
- Binance API
- VNStock API
- BeautifulSoup / Selenium

### 🔹 Backend
- FastAPI / Flask

### 🔹 Visualization
- Matplotlib
- Seaborn
- Plotly

### 🔹 DevOps
- Docker
- GitHub Actions

### 🔹 Methodology
- Agile / Scrum

---

## 📂 Project Structure


project-root/
│
├── data/
│ ├── raw/
│ ├── processed/
│
├── src/
│ ├── crawler/
│ ├── preprocessing/
│ ├── features/
│ ├── models/
│ ├── evaluation/
│ ├── api/
│
├── notebooks/
├── tests/
├── configs/
│
├── requirements.txt
├── README.md


---

# 🌿 Git Workflow

## Branch Strategy


main
develop
feature/*


---

## 🔹 Branch Roles

### `main`
- Production ổn định
- Chỉ merge từ `develop`
- ❌ Không commit trực tiếp

---

### `develop`
- Nhánh phát triển chính
- Tích hợp feature
- Test hệ thống

---

### `feature/*`
Ví dụ:


feature/binance-crawler
feature/data-cleaning
feature/xgboost-model
feature/lstm-model
feature/api
feature/dashboard


---

## 🔄 Workflow


feature/*
↓
Pull Request
↓
develop
↓
test
↓
main


---

# 👥 Team Rules

## 1. Không commit vào `main`

---

## 2. Tạo branch trước khi code

```bash
git checkout develop
git pull origin develop
git checkout -b feature/<name>
3. Pull code mới nhất
git checkout develop
git pull origin develop
4. Commit thường xuyên
Nhỏ, rõ ràng
Không gom nhiều thứ vào 1 commit
5. Không commit file nhạy cảm
.env
API keys
secret tokens
dataset lớn
model đã train
6. Test trước khi merge
Code chạy OK
Không phá chức năng cũ
Không log/debug thừa
