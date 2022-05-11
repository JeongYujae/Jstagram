from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib import messages
from .models import Tag, Post
from django.contrib.auth import get_user_model

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
    return render(request, 'jstagram/post_detail.html',{
        "post":post
    })


def user_page(request, username):
    page_user=get_object_or_404(get_user_model(),username=username, is_active=True)
    post_list=Post.objects.filter(author=page_user)
    post_list_count=post_list.count() # 실제 db에 count 쿼리 전송
    return render(request, "jstagram/user_page.html",{
        "page_user":page_user,
        "post_list":post_list,
        'post_list_count':post_list_count
    })