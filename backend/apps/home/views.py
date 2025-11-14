from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Category,
    FeaturedCourse,
    HeroContent,
    HomeStatistic,
    InstructorProfile,
    Testimonial,
)
from .serializers import (
    CategoryCardSerializer,
    CourseCardSerializer,
    HeroContentSerializer,
    HomeStatisticSerializer,
    InstructorCardSerializer,
    TestimonialSerializer,
)
from .services import (
    get_statistics,
    get_testimonials,
    get_top_categories,
    get_top_courses,
    get_top_instructors,
)


def seed_home_content():
    if not HeroContent.objects.exists():
        HeroContent.objects.create(
            headline="Nâng Cao Kĩ Năng Với Hướng Dẫn Chuyên Nghiệp",
            sub_headline="Kết nối với những tutor giỏi tại HCMUT, được ghép đôi theo nhu cầu cá nhân.",
            primary_cta="BẮT ĐẦU NGAY",
            secondary_cta="TÌM HIỂU THÊM",
        )

    if not HomeStatistic.objects.exists():
        HomeStatistic.objects.bulk_create(
            [
                HomeStatistic(label="Sinh viên tham gia", value="5000+", order=1),
                HomeStatistic(label="Mentor/Tutor", value="250+", order=2),
                HomeStatistic(label="Khóa học/Diễn đàn", value="500+", order=3),
                HomeStatistic(label="Đánh giá", value="4.8", order=4),
            ]
        )

    if not Category.objects.exists():
        Category.objects.bulk_create(
            [
                Category(
                    title="Vật Lý 1",
                    description="11 courses",
                    total_courses=11,
                ),
                Category(
                    title="Nhập môn Kỹ thuật",
                    description="12 courses",
                    total_courses=12,
                ),
                Category(
                    title="Giải tích",
                    description="12 courses",
                    total_courses=12,
                ),
                Category(
                    title="Hóa đại cương",
                    description="14 courses",
                    total_courses=14,
                ),
            ]
        )

    if not FeaturedCourse.objects.exists():
        category = Category.objects.first()
        FeaturedCourse.objects.create(
            title="Beginner’s Guide to Design",
            instructor="Ronald Richards",
            hours=22,
            lectures=155,
            level="Beginner",
            rating=5,
            rating_count=1200,
            category=category,
        )

    if not InstructorProfile.objects.exists():
        InstructorProfile.objects.create(
            name="Ronald Richards",
            title="UI/UX Designer",
            total_students=1200,
        )

    if not Testimonial.objects.exists():
        Testimonial.objects.create(
            quote="Byway’s tech courses are top-notch!",
            author="Jane Doe",
            job_title="Designer",
        )


class StatisticsAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        seed_home_content()
        statistics = get_statistics()
        serializer = HomeStatisticSerializer(statistics, many=True)
        return Response(serializer.data)


class TopCategoriesAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        seed_home_content()
        categories = get_top_categories()
        serializer = CategoryCardSerializer(categories, many=True)
        return Response(serializer.data)


class TopCoursesAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        seed_home_content()
        courses = get_top_courses()
        serializer = CourseCardSerializer(courses, many=True)
        return Response(serializer.data)


class TopInstructorsAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        seed_home_content()
        instructors = get_top_instructors()
        serializer = InstructorCardSerializer(instructors, many=True)
        return Response(serializer.data)


class TestimonialsAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        seed_home_content()
        testimonials = get_testimonials()
        serializer = TestimonialSerializer(testimonials, many=True)
        return Response(serializer.data)


class HomeSummaryView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        seed_home_content()
        hero = HeroContent.objects.filter(is_active=True).first()
        hero_data = HeroContentSerializer(hero).data if hero else {}

        stats = HomeStatisticSerializer(
            HomeStatistic.objects.filter(is_active=True).order_by("order"),
            many=True,
        ).data

        categories = CategoryCardSerializer(
            Category.objects.filter(is_featured=True)[:4], many=True
        ).data

        courses = CourseCardSerializer(
            FeaturedCourse.objects.filter(is_featured=True)[:3], many=True
        ).data

        instructors = InstructorCardSerializer(
            InstructorProfile.objects.filter(is_featured=True)[:3], many=True
        ).data

        testimonials = TestimonialSerializer(
            Testimonial.objects.filter(is_featured=True)[:2], many=True
        ).data

        return Response(
            {
                "hero": hero_data,
                "statistics": stats,
                "categories": categories,
                "courses": courses,
                "instructors": instructors,
                "testimonials": testimonials,
            }
        )


class HomeTemplateView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        seed_home_content()
        context = super().get_context_data(**kwargs)
        context["statistics"] = HomeStatistic.objects.filter(is_active=True)
        context["categories"] = Category.objects.filter(is_featured=True)[:4]
        context["courses"] = FeaturedCourse.objects.filter(is_featured=True)[:3]
        context["instructors"] = InstructorProfile.objects.filter(is_featured=True)[:3]
        context["testimonials"] = Testimonial.objects.filter(is_featured=True)[:2]
        context["session_user"] = self.request.session.get("full_name")
        return context

