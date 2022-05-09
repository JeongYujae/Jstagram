from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

urlpatterns=[
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/', views.password_change, name='password_change'),
    path('logout/', views.logout, name='logout'),
    path('edit/', views.profile_edit, name='profile_edit'),
]
