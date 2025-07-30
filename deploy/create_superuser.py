#!/usr/bin/env python
"""
Script để tạo superuser nếu chưa tồn tại
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dh_index.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def create_superuser():
    username = 'dh'
    email = 'dh@gmail.com'
    password = '123'
    full_name = 'DH Admin'

    # Kiểm tra xem user đã tồn tại chưa
    if User.objects.filter(username=username).exists():
        print(f"Superuser '{username}' đã tồn tại. Bỏ qua việc tạo mới.")
        return

    # Tạo superuser mới
    try:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            full_name=full_name
        )
        print(f"Đã tạo superuser thành công: {username}")
    except Exception as e:
        print(f"Lỗi khi tạo superuser: {e}")

if __name__ == '__main__':
    create_superuser()
