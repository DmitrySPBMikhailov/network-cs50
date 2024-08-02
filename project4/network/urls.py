
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('show-user-profile/<int:pk>', views.show_user_profile, name='show_user_profile'),
    path('show-following', views.show_following, name='show_following'),
    path('toggle-following', views.toggle_following, name='toggle_following'),
    path('edit-post', views.edit_post, name='edit_post'),
    path('toggle-likes', views.toggle_likes, name='toggle_likes'),
]
