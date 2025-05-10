from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('post/list/', views.post_list, name='post_list'),
    path('post/list/<str:year>/<int:month>/<int:day>/<slug:post_slug>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:year>/<int:month>/<int:day>/<slug:post_slug>/', views.profile_comments, name='profile-comments')
]