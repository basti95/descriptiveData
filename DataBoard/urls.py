from .views import index, get_data, handle_bot_message
from django.urls import path

urlpatterns = [
    path('', index),
    path('get_data/', get_data),
    path('bot_message_api/', handle_bot_message),
]
