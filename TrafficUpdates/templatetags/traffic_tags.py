from django import template
from django.contrib.auth.models import User
from django_gravatar.helpers import get_gravatar_url, has_gravatar

register = template.Library()

@register.filter
def gravatar_exists(user):
	exists = has_gravatar(user.email)
	return exists
