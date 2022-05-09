from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractUser):
    website_url=models.URLField(blank= True)
    bio= models.TextField(blank= True)
    phone_number=models.CharField(validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")], max_length=13)
    avatar=models.ImageField(blank=True, upload_to="accounts/avatar/%Y/%m/%d", help_text="48px * 48px png or jpg needed")

    # def send_welcome_email(self):
    #     subject= render_to_string("accounts/welcome_email_subject.txt",{
    #         "user":self
    #     })
    #     content=render_to_string("accounts/welcome_email_content.txt",{
    #         "user":self
    #     })
    #     sender_email=settings.WELCOME_EMAIL_SENDER
    #     send_mail(subject, content, sender_email, [self.email], fail_silently=False)