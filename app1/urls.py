# app1/urls.py
from django.urls import path
from .views import full_blog_post,view_blog_posts,profile_page,create_blog_post,edit_blog_post, LogoutPage, LoginPage, HomePage, SignupPage, doctor_dashboard


urlpatterns = [
    path('', SignupPage, name='signup'),
    path('login/', LoginPage, name='login'),
    path('home/', HomePage, name='home'),
    path('logout/', LogoutPage, name='logout'),
    path('doctor_dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('create_blog_post/', create_blog_post, name='create_blog_post'),
    path('edit_blog_post/<int:post_id>/', edit_blog_post, name='edit_blog_post'),
    path('view_blog_posts/', view_blog_posts, name='view_blog_posts'),
    path('view_blog_posts/<str:category>/', view_blog_posts, name='view_blog_posts_category'),
    path('profile/', profile_page, name='profile'),
    path('full_blog_post/<int:post_id>/', full_blog_post, name='full_blog_post'),
]