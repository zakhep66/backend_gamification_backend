from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, EmployeeViewSet, ProfileView, ShortStudentInfoViewSet

router = DefaultRouter()
router.register(r'student', StudentViewSet, basename='student')
router.register(r'short_student', ShortStudentInfoViewSet, basename='short_student')
router.register(r'employee', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProfileView.as_view(), name='profile'),
]
