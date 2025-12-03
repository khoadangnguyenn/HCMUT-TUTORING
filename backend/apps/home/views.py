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


def get_avatar_url_by_role(role):
    """
    Get avatar URL based on user role.
    Maps role to corresponding avatar file in home/resources/
    """
    avatar_map = {
        'student': '/static/home/resources/student-avatar.jpg',
        'tutor': '/static/home/resources/tutor-avatar.jpg',
        'manager': '/static/home/resources/manager-avatar.jpg',
    }
    return avatar_map.get(role, '/static/home/resources/student-avatar.png')


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
        
        # Get avatar URL based on user role from session
        user_role = self.request.session.get('role', 'student')
        context["avatar_url"] = get_avatar_url_by_role(user_role)
        context["user_role"] = user_role
        
        return context

