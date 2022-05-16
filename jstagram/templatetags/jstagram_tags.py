#html 구조에서는 인자를 포함하는 전송하는 문법을 지원하지 X
#그래서 이 파일에서 함수를 만들고 html에서 이 함수를 호출할 계획(필터)

from django import template


register=template.Library()

@register.filter
def is_like_user(post, user):
    return post.is_like_user(user)