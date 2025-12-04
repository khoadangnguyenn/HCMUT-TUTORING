from rest_framework import serializers

from .models import (
    Category,
    FeaturedCourse,
    HeroContent,
    HomeStatistic,
    InstructorProfile,
    Testimonial,
)


class HeroContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroContent
        fields = [
            "id",
            "headline",
            "sub_headline",
            "primary_cta",
            "secondary_cta",
            "background_image",
        ]


class HomeStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeStatistic
        fields = ["id", "label", "value", "order"]


class CategoryCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "description", "image", "total_courses", "is_featured"]


class CourseCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedCourse
        fields = [
            "id",
            "title",
            "instructor",
            "hours",
            "lectures",
            "level",
            "rating",
            "rating_count",
            "image",
        ]


class InstructorCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorProfile
        fields = ["id", "name", "title", "avatar", "bio", "rating", "total_students"]


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["id", "quote", "author", "job_title", "is_featured", "created_at"]