from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HeroContent(TimestampedModel):
    headline = models.CharField(max_length=255)
    sub_headline = models.TextField()
    primary_cta = models.CharField(max_length=120, default="Bắt đầu ngay")
    secondary_cta = models.CharField(max_length=120, blank=True)
    background_image = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Hero content"
        verbose_name_plural = "Hero content"


class HomeStatistic(TimestampedModel):
    label = models.CharField(max_length=120)
    value = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]


class Category(TimestampedModel):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True)
    image = models.URLField(blank=True)
    total_courses = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ["-total_courses"]


class FeaturedCourse(TimestampedModel):
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    hours = models.PositiveIntegerField(default=0)
    lectures = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=50, default="Beginner")
    image = models.URLField(blank=True)
    rating = models.FloatField(default=5.0)
    rating_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="courses"
    )
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]


class InstructorProfile(TimestampedModel):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    avatar = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    rating = models.FloatField(default=4.8)
    total_students = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ["-rating"]


class Testimonial(TimestampedModel):
    quote = models.TextField()
    author = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150, blank=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]


