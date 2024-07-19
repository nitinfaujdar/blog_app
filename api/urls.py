from django.urls import path
from .views import *

urlpatterns = [
    path('blog/', BlogsView.as_view(), name='blog'),
    path('like/', LikeBlogsView.as_view(), name='like'),
    path('comment/', CommentView.as_view(), name='comment'),
]
