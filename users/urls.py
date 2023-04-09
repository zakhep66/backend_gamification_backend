from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .user_views import StudentViewSet, EmployeeViewSet, ProfileView, ShortStudentInfoViewSet
from .views import DirectionViewSet

router = DefaultRouter()
router.register(r'student', StudentViewSet, basename='student')
router.register(r'short_student', ShortStudentInfoViewSet, basename='short_student')
router.register(r'employee', EmployeeViewSet, basename='employee')
router.register(r'direction', DirectionViewSet, basename='direction')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProfileView.as_view(), name='profile'),
]
