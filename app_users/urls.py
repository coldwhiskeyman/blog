from django.urls import path

from app_users import views


urlpatterns = [
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('register', views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>', views.UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/update', views.UserUpdateView.as_view(), name='user_update'),
]
