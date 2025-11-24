import os
from pymongo import MongoClient
from pathlib import Path
import django

# --- Setup Django ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings

# --- Kết nối MongoDB ---
client = MongoClient(settings.MONGO_URL)

# --- Xoá toàn bộ database ---
client.drop_database(settings.MONGO_NAME)
print(f"Database '{settings.MONGO_NAME}' đã bị xóa.")

# --- Xoá các migration cũ (tuỳ chọn) ---
apps = ["login", "home", "forgetpassword", "roleselect"]
for app in apps:
    migrations_path = Path(__file__).resolve().parent / app / "migrations"
    if migrations_path.exists():
        for f in migrations_path.iterdir():
            if f.is_file() and f.name != "__init__.py":
                f.unlink()
        print(f"Migration cũ của app '{app}' đã bị xóa.")

# --- Tạo migration mới và migrate ---
os.system("python3.11 manage.py makemigrations")
os.system("python3.11 manage.py migrate")