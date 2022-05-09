from django.shortcuts import redirect, render
from .forms import SignupForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login


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

