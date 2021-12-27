from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blogs/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('subscribes/', views.SubscribesView.as_view(), name='subscribes'),
    path('subscribes/add/<int:pk>', views.SubscribesAddView.as_view(), name='subscribes-add'),
    path('subscribes/delete/<int:pk>', views.SubscribeDeleteView.as_view(), name='subscribe-delete'),
    path('personal/', views.PersonalView.as_view(), name='personal'),
    path('personal/posts', views.PersonalPostView.as_view(), name='personal-post'),
    path('post/<int:pk>', views.PostView.as_view(), name='post-detail'),
    path('post/create/', views.CreatePostView.as_view(), name='post-create'),
    path('post/update/<int:pk>', views.PostUpdate.as_view(), name='post-update'),
    path('post/delete/<int:pk>', views.PostDelete.as_view(), name='post-delete'),
    path('post/addreadhistory/<int:pk>', views.AddPostReadHistory.as_view(), name='post-addreadhistory'),

]
