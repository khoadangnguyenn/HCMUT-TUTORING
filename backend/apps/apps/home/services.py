from typing import Optional

from .models import Category, FeaturedCourse, HomeStatistic, InstructorProfile, Testimonial


def get_statistics(limit: Optional[int] = None):
    queryset = HomeStatistic.objects.filter(is_active=True).order_by("order")
    if limit is not None:
        queryset = queryset[:limit]
    return list(queryset)


def get_top_categories(limit: int = 4):
    return list(
        Category.objects.filter(is_featured=True)
        .order_by("-total_courses")[:limit]
    )


def get_top_courses(limit: int = 6):
    return list(
        FeaturedCourse.objects.filter(is_featured=True)
        .order_by("-rating", "-created_at")[:limit]
    )


def get_top_instructors(limit: int = 4):
    return list(
        InstructorProfile.objects.filter(is_featured=True).order_by("-rating")[:limit]
    )


def get_testimonials(limit: int = 6):
    return list(
        Testimonial.objects.filter(is_featured=True)
        .order_by("-created_at")[:limit]
    )