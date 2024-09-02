from django.urls import path
from . import views

app_name = "friends"

urlpatterns = [
    path('request/send', views.SendFriendRequest.as_view(), name="send-friend-request"),
    path('request/accept', views.AcceptFriendRequest.as_view(), name="accept-friend-request"),
    path('request/reject', views.RejectFriendRequest.as_view(), name="reject-friend-request"),
    path('all', views.FriendsList.as_view(), name="all-friends"),
    path('pending-requests', views.PendingRequests.as_view(), name="pending-friend-request")
]

