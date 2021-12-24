from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView

from . import models
from .forms import CreateForm


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = models.Blog.objects.select_related('user')
        if self.request.user.is_authenticated:
            query = query.exclude(user=self.request.user)
        context['blogs'] = query.all()
        return context


class PostView(TemplateView):
    template_name = 'main/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = models.Post.objects.get(pk=kwargs['pk'])
        return context


class BlogDetailView(DetailView):
    model = models.Blog
    template_name = 'main/blog_detail.html'
    context_object_name = 'blog'


class SubscribesView(TemplateView):
    template_name = 'main/subscribes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribes'] = (
            models.Subscription.objects
                .select_related('user')
                .filter(user=self.request.user)
                .prefetch_related('blog')
        )
        return context


class SubscribeDeleteView(View):
    def get(self, request, pk):
        subscribe = models.Subscription.objects.get(id=pk)
        subscribe.delete()
        return redirect('main:subscribes')


class PersonalView(TemplateView):
    template_name = 'main/personal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personal'] = models.Post.objects.filter(blog__user=self.request.user)
        context['posts'] = (
            models.Post.objects
                .filter(blog__subscription__user=self.request.user)
                .order_by('-post_time')
        )
        return context


class CreatePostView(CreateView):
    template_name = 'main/create_post.html'
    form_class = CreateForm
    success_url = '/'


class PostUpdate(UpdateView):
    model = models.Post
    fields = ['title', 'content']


class PostDelete(View):
    def get(self, request, pk):
        post = models.Post.objects.get(id=pk)
        if request.user.is_authenticated:
            pass
