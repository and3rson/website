from django.shortcuts import render, get_object_or_404
from dunai.posts.models import Post
from django.core.urlresolvers import reverse
from dunai.website.models import Contact
from .helpers import get_share_count


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

    if 'HTTP_X_FORWARDED_FOR' in request.META:
        post.add_view(request.META['HTTP_X_FORWARDED_FOR'])
        post.save()

    likes = get_share_count(request.build_absolute_uri(post_slug))

    # next_post = Post.objects.filter(date_added__gt=post.date_added).order_by('date_added').prefetch_related('categories').first()
    # prev_post = Post.objects.filter(date_added__lt=post.date_added).order_by('-date_added').prefetch_related('categories').first()
    other_posts = Post.objects.exclude(pk=post.pk).order_by('?')[:3]

    return render(request, 'dunai/post.jade', dict(
        contacts=Contact.objects.order_by('order'),
        post=post,
        likes=likes,
        # prev_post=prev_post,
        # next_post=next_post,
        other_posts=other_posts,
        breadcrumbs=[
            dict(title='Andrew Dunai', url=reverse('website:index')),
            dict(title='Posts', url=reverse('posts:list')),
            dict(title=post.title, url=post.get_absolute_url()),
        ],
        page='posts'
    ))
