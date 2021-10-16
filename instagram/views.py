from django.shortcuts import render,redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request, 'instagram/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'instagram/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post
    template_name = 'instagram/post_detail.html'
    context_object_name = 'post'
    
def post(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author= user,
                content=form.cleaned_data["content"],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post).order_by('-date_posted')
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }

    return self.get(self, request, pk, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'instagram/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'image', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'instagram/post_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
        
def about(request):
    return render(request,'instagram/about.html',)

def like(request,pk):
    post = Post.objects.get(pk=pk)
    post.likes+=1
    post.save()
    return redirect('instagram-home')