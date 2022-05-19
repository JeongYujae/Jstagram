import re
from django.db import models
from django.conf import settings
from django.urls import reverse


class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True

class Post(BaseModel):
    author=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_post_set',on_delete=models.CASCADE) #충돌이 일어나서 related_name으로 migrations에서 충돌 피할 수 있음
    photo=models.ImageField(upload_to="jstagram/post/%Y/%m/%d")
    caption=models.CharField(max_length=500)
    tag_set=models.ManyToManyField('Tag', blank=True)
    location=models.CharField(max_length=100) 
    like_user_set=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_post_set', blank=True)

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse("jstagram:post_detail", kwargs={"pk": self.pk})

    def extract_tag_list(self): #caption에서 #뽑아내는 함수
        tag_name_list=re.findall(r"#([a-zA-Z\dㄱ-힣]+)",self.caption)  
        tag_list=[]
        for tag_name in tag_name_list:
            tag, _=Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def get_absolute_url(self):
        return reverse("jstagram:post_detail", args=[self.pk])

    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()

    class Meta:
        ordering=['-id']


    
class Comment(BaseModel):
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    message=models.TextField()

    class Meta:
        ordering=['-id']

        


class Tag(models.Model):
    name=models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name