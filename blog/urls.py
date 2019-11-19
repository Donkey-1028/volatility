from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', home, name='home'),
    path('index', index, name='index'),
    path('add', post_create, name='add'),
    path('update/<int:pk>', post_update, name='update'),
    path('delete/<int:pk>', post_delete, name='delete'),
    path('detail/<int:pk>', detail, name='detail'),
    path('comment_delete/<int:pk>', comment_delete, name='comment_delete'),
]