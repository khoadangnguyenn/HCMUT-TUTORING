from django.urls import path

from .views import (
    HomeSummaryView,
    HomeTemplateView,
    StatisticsAPI,
    TestimonialsAPI,
    TopCategoriesAPI,
    TopCoursesAPI,
    TopInstructorsAPI,
)

app_name = "home"

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="landing_page"),
    path("summary/", HomeSummaryView.as_view(), name="summary"),
    path("statistics/", StatisticsAPI.as_view(), name="statistics"),
    path("categories/top/", TopCategoriesAPI.as_view(), name="categories_top"),
    path("courses/top/", TopCoursesAPI.as_view(), name="courses_top"),
    path("instructors/top/", TopInstructorsAPI.as_view(), name="instructors_top"),
    path("testimonials/", TestimonialsAPI.as_view(), name="testimonials"),
]