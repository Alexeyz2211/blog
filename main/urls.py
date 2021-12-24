from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blogs/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('subscribes/', views.SubscribesView.as_view(), name='subscribes'),
    path('personal/', views.PersonalView.as_view(), name='personal'),
    path('post/<int:pk>', views.PostView.as_view(), name='post-detail'),
    path('create/', views.CreatePostView.as_view(), name='post-create'),
    path('subscribes/delete/<int:pk>', views.SubscribeDeleteView.as_view(), name='subscribe-delete'),

]
