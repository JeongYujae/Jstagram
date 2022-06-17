from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.contrib import messages
from .models import Tag, Post
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
@login_required
def index(request):
    timesince=timezone.now() - timedelta(days=3)
    post_list=Post.objects.all().filter(Q(author=request.user) | Q(author__in=request.user.following_set.all())).filter(created_at__gte=timesince)
    suggested_user_list=get_user_model().objects.all().exclude(pk=request.user.pk).exclude(pk__in=request.user.following_set.all())[:3]
    comment_form=CommentForm()
    return render(request, "jstagram/index.html",{
        "suggested_user_list": suggested_user_list,
        "post_list":post_list,
        "comment_form":comment_form,
        
    })

@login_required
def post_new(request):
    if request.method=='POST':
        form=PostForm(request.POST, request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(request, 'Succesfully Saved')
            return redirect(post)
    else:
        form=PostForm()

    return render(request,"jstagram/post_form.html",{
        "form":form,
    })


def post_detail(request, pk):
    post=get_object_or_404(Post,pk=pk)
    comment_form=CommentForm() #빈 폼을 생성(literally 네모 칸을 하나 만듦)
    return render(request, 'jstagram/post_detail.html',{
        "post":post,
        "comment_form": comment_form,
    })

@login_required
def post_like(request, pk):
    post=get_object_or_404(Post,pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, f"Like the #{post.pk}")
    redirect_url=request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

@login_required
def post_unlike(request, pk):
    post=get_object_or_404(Post,pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f"Unlike the #{post.pk}")
    redirect_url=request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return render(request, "jstagram/_comment.html", {
                    "comment": comment,
                })
            return redirect(comment.post)
    else:
        form = CommentForm()
    return render(request, "jstagram/comment_form.html", {
        "form": form,
    })


# @login_required
# def comment_new(request, post_pk):
#     post=get_object_or_404(Post,pk=post_pk)
    
#     if request.method=='POST':
#         form=CommentForm(request.POST, request.FILES)
#         if form.is_valid():
#             comment=form.save(commit=False)
#             comment.post= post
#             comment.author=request.user
#             comment.save()
#             if request.is_ajax():
#                 return render(request,"jstagram/_comment.html",{
#                     "comment": comment,
#                 })
#             return redirect(comment.post)
#     else:
#         form= CommentForm()
#     return render(request, "jstagram/comment_form.html",{
#         "form":form
#     })


def user_page(request, username):
    page_user=get_object_or_404(get_user_model(),username=username, is_active=True)
    post_list=Post.objects.filter(author=page_user)
    post_list_count=post_list.count() # 실제 db에 count 쿼리 전송   

    if request.user.is_authenticated:
        is_follow=request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow=False
    return render(request, "jstagram/user_page.html",{
        "page_user":page_user,
        "post_list":post_list,
        'post_list_count':post_list_count,
        "is_follow":is_follow
    })