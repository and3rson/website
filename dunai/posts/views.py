from django.shortcuts import render, get_object_or_404
from dunai.posts.models import Post
from django.core.urlresolvers import reverse
from dunai.website.models import Contact


def view_posts(request):
    posts = Post.objects.order_by('-date_added').prefetch_related('categories')
    return render(request, 'dunai/posts.jade', dict(
        contacts=Contact.objects.order_by('order'),
        posts=posts,
        breadcrumbs=[
            dict(title='Andrew Dunai', url=reverse('website:index')),
            dict(title='Posts', url=reverse('posts:list')),
        ],
        page='posts'
    ))


def view_post(request, post_slug):
    post = get_object_or_404(Post.objects.prefetch_related('categories'), slug=post_slug)

    return render(request, 'dunai/post.jade', dict(
        contacts=Contact.objects.order_by('order'),
        post=post,
        breadcrumbs=[
            dict(title='Andrew Dunai', url=reverse('website:index')),
            dict(title='Posts', url=reverse('posts:list')),
            dict(title=post.title, url=post.get_absolute_url()),
        ],
        page='posts'
    ))
