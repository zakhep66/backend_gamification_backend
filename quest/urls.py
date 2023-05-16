from django.urls import path, include
from rest_framework.routers import DefaultRouter

from quest.views import QuestViewSet, QuestTypeViewSet

router = DefaultRouter()
router.register(r'quest', QuestViewSet, basename='quest')
router.register(r'quest_type', QuestTypeViewSet, basename='quest_type')

urlpatterns = [
    path('', include(router.urls)),
]
