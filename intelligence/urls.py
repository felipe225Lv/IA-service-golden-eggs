from django.urls import path
from intelligence.views import ConversationList

urlpatterns = [
    path('history/', ConversationList.as_view(), name='history'),
]
