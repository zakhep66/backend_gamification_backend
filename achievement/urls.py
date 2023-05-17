from django.urls import path, include
from rest_framework.routers import DefaultRouter

from achievement.views import AchievementViewSet

router = DefaultRouter()
router.register(r'achievement', AchievementViewSet, basename='achievement')
student_achievement = AchievementViewSet.as_view({'post': 'student_achievement'}, basename='student_achievement')


urlpatterns = [
    path('', include(router.urls)),
    path('achievement/student_achievement', student_achievement, name='student_achievement')
]
