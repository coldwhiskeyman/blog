from django.urls import path

from blog.views import (
    PostCreateView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    PostUploadView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('upload', PostUploadView.as_view(), name='post_upload'),
    path('add', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>', PostDetailView.as_view(), name='post_details'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
]
