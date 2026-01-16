from django.urls import path
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('<int:pk>/edit/', BlogUpdateView.as_view(), name='blog_edit'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
]
