from django.core.management.base import BaseCommand
from apps.login.models import User, UserRole


class Command(BaseCommand):
    help = 'Create 3 demo users for each role: student, tutor, manager'

    def handle(self, *args, **options):
        users_data = [
            # Students
            {
                'email': 'student@example.com',
                'full_name': 'Student Khoa',
                'password': 'student123',
                'role': UserRole.STUDENT,
                'bio': 'Sinh viên năm 2 Khoa Máy Tính',
            },
            # Tutors
            {
                'email': 'tutor@example.com',
                'full_name': ' Tutor Khoa',
                'password': 'tutor123',
                'role': UserRole.TUTOR,
                'bio': 'Tutor môn Lập trình, Toán học',
            },
            # Managers
            {
                'email': 'manager@example.com',
                'full_name': 'Manager Khoa',
                'password': 'manager123',
                'role': UserRole.MANAGER,
                'bio': 'Quản lý hệ thống HCMUT Tutoring',
            },
        ]

        created_count = 0
        for user_data in users_data:
            email = user_data['email']
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(f'✓ User "{email}" đã tồn tại, bỏ qua')
                )
                continue

            user = User.objects.create(
                email=email,
                full_name=user_data['full_name'],
                role=user_data['role'],
                bio=user_data['bio'],
            )
            user.set_password(user_data['password'])
            user.save()
            created_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Tạo user thành công: {email}\n'
                    f'  Mật khẩu: {user_data["password"]}\n'
                    f'  Vai trò: {user_data["role"]}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Hoàn thành tạo {created_count} tài khoản test!')
        )
