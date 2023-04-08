from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, EmployeeViewSet, ProfileView  # , ShortStudentInfoViewSet

router = DefaultRouter()
router.register(r'student', StudentViewSet)
router.register(r'employee', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProfileView.as_view(), name='profile'),
]
