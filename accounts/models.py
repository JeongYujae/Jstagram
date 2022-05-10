from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.validators import RegexValidator
from django.shortcuts import resolve_url

# Create your models here.

class User(AbstractUser):
    website_url=models.URLField(blank= True)
    bio= models.TextField(blank= True)
    phone_number=models.CharField(validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")], max_length=13)
    avatar=models.ImageField(blank=True, upload_to="accounts/avatar/%Y/%m/%d", help_text="48px * 48px png or jpg needed")


    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url("pydenticon_image",self.username)
    # def send_welcome_email(self):
    #     subject= render_to_string("accounts/welcome_email_subject.txt",{
    #         "user":self
    #     })
    #     content=render_to_string("accounts/welcome_email_content.txt",{
    #         "user":self
    #     })
    #     sender_email=settings.WELCOME_EMAIL_SENDER
    #     send_mail(subject, content, sender_email, [self.email], fail_silently=False)