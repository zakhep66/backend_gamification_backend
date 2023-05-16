from django.urls import path, include
from rest_framework.routers import DefaultRouter

from quest.views import QuestViewSet, QuestTypeViewSet

router = DefaultRouter()
router.register(r'quest', QuestViewSet, basename='quest')
router.register(r'quest_type', QuestTypeViewSet, basename='quest_type')
all_is_active_quest = QuestViewSet.as_view({'get': 'all_is_active_quest'}, basename='all_is_active_quest')
student_quest = QuestViewSet.as_view({'post': 'student_quest'}, basename='student_quest')
employee_quest = QuestViewSet.as_view({'post': 'employee_quest'}, basename='employee_quest')

urlpatterns = [
    path('', include(router.urls)),
    path('quest/all_is_active_quest', all_is_active_quest, name='all_is_active_quest'),
    path('quest/student_quest', student_quest, name='student_quest'),
    path('quest/employee_quest', employee_quest, name='employee_quest'),
]
