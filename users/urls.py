from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, EmployeeViewSet

router = DefaultRouter()
router.register(r'student', StudentViewSet)
router.register(r'employee', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
