from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib import messages
from .models import Tag

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
            return redirect("/")
    else:
        form=PostForm()

    return render(request,"jstagram/post_form.html",{
        "form":form,
    })
