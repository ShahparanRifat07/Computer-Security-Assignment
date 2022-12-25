
from django.urls import path
from .views import signup,signin,verify,home,profile,post_blog,edit_blog,delete_blog,user_logout,profile,blog_detail,admin, unsecure_login

urlpatterns = [
    path('',home,name="home"),
    path('signup/',signup,name="signup"),
    path('login/',signin,name="login"),
    path('unsecure_login/',unsecure_login,name="unsecure_login"),
    path('logout/',user_logout,name="logout"),
    path('verify/',verify,name="verify"),
    path('profile/<int:pk>/',profile,name="profile"),
    path('create_blog/',post_blog,name="post_blog"),
    path('blog_detail/<int:pk>/',blog_detail,name="blog_detail"),
    path('edit_blog/<int:pk>/',edit_blog,name="edit_blog"),
    path('delete_blog/<int:pk>/',delete_blog,name="delete_blog"),
    path('admin/',admin,name="admin"),
]