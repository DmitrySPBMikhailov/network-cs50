from django import template

register = template.Library()

@register.filter
def did_user_liked(post, user_id):
    return post.user_liked_this.filter(id=user_id).count()