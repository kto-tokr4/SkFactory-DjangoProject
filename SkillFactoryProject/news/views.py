from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import PostForm, CommentForm
from account.models import Profile


def post_list(request):
    post_list = Post.objects.all().order_by('-created')
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.
                               num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request,
                  'news/post_list.html',
                  {'posts': posts})


@login_required()
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print (request.FILES)
            post = form.save(commit=False)
            post.author = Profile.objects.get(user=request.user)
            post.save()
            return redirect('news:post_list')
    else:
        form = PostForm()
    return render(request,
                  'news/post_create.html',
                  {'form': form})


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post,
                             slug=post_slug,
                             created__year=year,
                             created__month=month,
                             created__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = Profile.objects.get(user=request.user)
            comment.post = post
            comment.save()
            post_author_email = post.author.user.email
            subject = f'Новый коментарий к посту {post.title}'
            message = f'Пользователь с ником {request.user.username} оставил новый коментарий.'
            send_mail(subject=subject,
                      message=message,
                      from_email='',
                      recipient_list=[post_author_email, ])

    return render(request,
                  'news/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,})


def profile(request):
    user = User.objects.get(username=request.user)
    user_posts = Post.objects.filter(author__user=user)
    paginator = Paginator(user_posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.
                               num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request,
                  'news/profile.html',
                  {'posts': posts})


def profile_comments(request, year, month, day, post_slug):
    post = get_object_or_404(Post,
                             slug=post_slug,
                             created__year=year,
                             created__month=month,
                             created__day=day)
    comments = post.comments.all()

    if request.method == "POST":
        comment = get_object_or_404(Comment, id=request.POST['comment_id'])
        comment.active = True
        comment.save()
        comment_author = comment.author.user

        subject = 'Публикация комментацрия'
        message = f'Ваш комментарий для поста {post.title} был опубликован его автором'
        send_mail(subject=subject,
                  message=message,
                  from_email='',
                  recipient_list=[comment_author.email,])

    return render(request, 'news/profile_post.html', {'post': post, 'comments': comments})
