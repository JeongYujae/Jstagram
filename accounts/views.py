from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .forms import SignupForm
from django.contrib import messages

def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            messages.success(request, "Thank you for sign up")
            next_url=request.GET.get('next','/')
            return redirect(next_url)
    else:
        form=SignupForm()
    return render(request, 'accounts/signup_form.html',{
        'form':form,
    })
