from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include

urlpatterns=[
    url(r'^$',views.index,name = 'index'),
    url(r'^register/',views.register,name = 'register'),
    url(r'^login/',auth_views.LoginView.as_view(template_name='users/login.html'),name = 'login'),
    url(r'^logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name = 'logout'),
    url(r'^profile/',views.profile,name = 'profile'),
    url(r'^update/',views.update,name = 'update'),
    url(r'^image/(\d+)',views.image,name ='image'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^comment/(?P<image_id>\d+)', views.comment, name='comment'),    
    path('like', views.like_post,name = 'like-post'),
    path('user_profile/<username>/', views.user_profile, name='user_profile'),
    path('unfollow/<to_unfollow>', views.unfollow, name='unfollow'),
    path('follow/<to_follow>', views.follow, name='follow')
] 