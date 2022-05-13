from django.urls import path, re_path
from . import views
# from django.contrib.auth import views as auth_views

urlpatterns=[
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/', views.password_change, name='password_change'),
    path('logout/', views.logout, name='logout'),
    path('edit/', views.profile_edit, name='profile_edit'),
    re_path(r'^(?P<username>[a-zA-Z\d+]+)/follow/$', views.user_follow, name='user_follow'),
    re_path(r'^(?P<username>[a-zA-Z\d+]+)/unfollow/$', views.user_unfollow, name='user_unfollow'),

]
