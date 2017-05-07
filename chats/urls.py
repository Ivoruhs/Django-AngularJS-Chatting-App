from django.conf.urls import url
from chats import views
from chats.views import *




urlpatterns = [
    url(r'^inbox/', views.inbox, name="inbox"),
]

#api urls
urlpatterns += [
    url(r'^api/userInfo', UserAPIView.as_view(), name="userInfo"),
    url(r'^api/allMessages', MessageAPIView.as_view(), name="allMessages"),
    url(r'^api/allConversations', ConversationAPIView.as_view(), name="allConversations"),
    url(r'^api/sendMessage', SendMessageAPIView.as_view())
]


urlpatterns += [
    url(r'^api/userConversation', UserConversationAPIView.as_view(), name="lastConvoHistory"),
    url(r'^api/userMeta', UserMetaAPIView.as_view(), name="userMeta")
]