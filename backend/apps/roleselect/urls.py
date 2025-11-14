from django.urls import path

from .views import RoleListView, RoleSelectionView

app_name = "roleselect"

urlpatterns = [
    path("", RoleListView.as_view(), name="list"),
    path("choose/", RoleSelectionView.as_view(), name="choose"),
]


