from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
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


class SubscribesView(LoginRequiredMixin, TemplateView):
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


class SubscribesAddView(View):
    def get(self, request, pk):
        user = request.user
        blog = models.Blog.objects.get(id=pk)
        models.Subscription.objects.get_or_create(blog=blog, user=user)
        return redirect('main:subscribes')


class SubscribeDeleteView(View):
    def get(self, request, pk):
        subscribe = models.Subscription.objects.get(id=pk)
        subscribe.delete()
        return redirect('main:subscribes')


class PersonalView(LoginRequiredMixin, TemplateView):
    template_name = 'main/personal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = (
            models.Post.objects
                .filter(blog__subscription__user=self.request.user)
                .order_by('-post_time')
        )
        readhistory = models.PostReadHistory.objects.filter(user=self.request.user)
        context['readposts'] = [h.post for h in readhistory]
        return context


class PersonalPostView(LoginRequiredMixin, TemplateView):
    template_name = 'main/personal_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = (
            models.Post.objects
                .filter(blog__user=self.request.user)
        )
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'main/create_post.html'
    form_class = CreateForm
    success_url = '/personal/posts'

    def form_valid(self, form):
        form.instance.blog = models.Blog.objects.get(user=self.request.user)
        return super(CreatePostView, self).form_valid(form)


class PostUpdate(UpdateView):
    model = models.Post
    fields = ['title', 'content']
    template_name_suffix = 'main/post_update_form'
    success_url = '/personal/posts'

    def form_valid(self, form):
        post = models.Post.objects.select_related('blog').select_related('blog__user').get(id=self.kwargs['pk'])
        if post.blog.user == self.request.user:
            return super(PostUpdate, self).form_valid(form)
        raise PermissionDenied()


class PostDelete(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = models.Post.objects.select_related('blog').select_related('blog__user').get(id=pk)
        if post.blog.user == self.request.user:
            post.delete()
            return redirect('main:personal-post')
        raise PermissionDenied()


class AddPostReadHistory(View):
    def get(self, request, pk):
        post = models.Post.objects.select_related('blog').get(id=pk)
        user = self.request.user
        subscription = models.Subscription.objects.get(blog=post.blog, user=user)
        models.PostReadHistory.objects.get_or_create(post=post, user=user, subscription=subscription)
        return redirect('main:personal')
