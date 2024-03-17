from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register', views.register, name="register"),
    path('login', views.login_view, name="login"),
    path('update', views.user_update, name='user_update'),

    path('profile/<int:id>/', views.profile_view, name='profile_view'),
    path('profile/update/<int:id>/', views.edit_profile, name='edit_profile'),
]