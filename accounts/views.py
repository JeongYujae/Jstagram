from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .forms import PasswordChangeForm, ProfileForm, SignupForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import User


login=LoginView.as_view(template_name='accounts/login_form.html')

def logout(request):
    messages.success(request, 'Log out completed')
    return logout_then_login(request)


def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            signed_user=form.save()
            auth_login(request, signed_user)
            messages.success(request, "Thank you for sign up")
            # signed_user.send_welcome_email()
            next_url=request.GET.get('next','/')
            return redirect(next_url)
    else:
        form=SignupForm()
    return render(request, 'accounts/signup_form.html',{
        'form':form,
    })


@login_required
def profile_edit(request):
    if request.method=='POST':
        form=ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile edited and saved succesfully!')
            return redirect('profile_edit')
    else:
        form=ProfileForm(instance=request.user)
    return render(request, "accounts/profile_edit_form.html",{
        "form":form
    })


class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    success_url=reverse_lazy("password_change")
    template_name='accounts/password_change_form.html'
    form_class=PasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, 'Changed Succesfully!')
        return super().form_valid(form)

password_change=PasswordChangeView.as_view()


@login_required
def user_follow(request,username):
    follow_user=get_object_or_404(User, username=username, is_active=True)
    request.user.following_set.add(follow_user) #내 계정을 남이 팔로우하니까 내 팔로잉 set에 추가
    follow_user.follower_set.add(request.user) #남이 내 계정을 팔로우하니까 남의 팔로워 set에 추가
    messages.success(request, f"Following {follow_user}")
    redirect_url=request.META.get("HTTP_REFERER","root")
    return redirect(redirect_url)


@login_required
def user_unfollow(request,username):
    unfollow_user=get_object_or_404(User, username=username, is_active=True)
    request.user.following_set.remove(unfollow_user) #내 계정을 남이 팔로우하니까 내 팔로잉 set에 추가
    unfollow_user.follower_set.remove(request.user) #남이 내 계정을 팔로우하니까 남의 팔로워 set에 추가
    messages.success(request, f"Unfollowing {unfollow_user}")
    redirect_url=request.META.get("HTTP_REFERER","root")
    return redirect(redirect_url)




