# CNPM-PROJECT

HCMUT-TUTORING

---

## 📝 Giới thiệu

Hệ thống sử dụng **Django** cho phần backend và **MongoDB** làm cơ sở dữ liệu NoSQL

---

## ✨ Tính năng chính

- **Xác thực người dùng:** Đăng ký, đăng nhập, đăng xuất.
- **Quản lý Sản phẩm/Bài viết:** Thêm, xóa, sửa, xem chi tiết các mục.
- **Giao diện RESTful API:** Cung cấp API để các ứng dụng khác có thể tương tác.

---

## 🛠️ Công nghệ sử dụng

- **Backend:** [Django](https://www.djangoproject.com/)
- **Cơ sở dữ liệu:** [MongoDB](https://www.mongodb.com/)
- **Thư viện kết nối DB:** [PyMongo](https://pymongo.readthedocs.io/en/stable/) (nếu kết nối thủ công) hoặc [Djongo](https://github.com/doctormo/djongo) (nếu tích hợp qua models)
- **Ngôn ngữ:** Python 3.x
- **Frontend:** HTML, CSS, JavaScript

---

HCMUTTUTORING-PROJECT/
│
├── backend/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── reset_db.py # Reset data MongoDB
│   │   ├── apps.py     # Override ObjectAutoFieldID
│   │   ├── urls.py     # Định nghĩa đường dẫn URL toàn cục 
│   │   ├── wsgi.py     # Cấu hình WSGI
│   │   ├── asgi.py     # Cấu hình ASGI
│   │
│   ├── apps/
│   │   ├── __init__.py
│   │   ├── login/
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   ├── services.py
│   │   │   ├── validators.py
│   │   │   ├── models.py
│   │   ├── home/
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   ├── services.py
│   │   │   ├── models.py
│   │   ├── forgetpassword/
│   │       ├── __init__.py
│   │       ├── apps.py
│   │       ├── urls.py
│   │       ├── views.py
│   │       ├── serializers.py
│   │       ├── services.py
│   │
│   ├── manage.py            # Script quản lý của Django
│   └── .env
│   └── README.md
├── frontend/
│   └── ...

## 🚀 Cài đặt và Chạy dự án

# Windows
```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
.\venv\Scripts\activate

# Khởi động dịch vụ MongoDB
net start MongoDB

# Cài đặt các gói phụ thuộc
pip install -r requirements.txt

#Tạo & chạy migration
python manage.py makemigrations
python manage.py migrate

# Tạo account để test
python manage.py seed_users

# Chạy server Django
python manage.py runserver
```

# macOS/Linux
```bash
# Tạo môi trường ảo
python3 -m venv venv

# Kích hoạt môi trường ảo
source venv/bin/activate

# Khởi động MongoDB (qua Homebrew)
brew services start mongodb-community@6.0

# Cài đặt các gói phụ thuộc
pip3 install -r requirements.txt

# Tạo & chạy migration
python3 manage.py makemigrations
python3 manage.py migrate

# Tạo account để test
python3 manage.py seed_users

# Chạy server Django
python3 manage.py runserver

```

