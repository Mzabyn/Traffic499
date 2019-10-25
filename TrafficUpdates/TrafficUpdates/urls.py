"""TrafficUpdates URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns

from post import views as post_view
from account import views as account_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^post/', post_view.posts, name='home'),
    url(r'^(?P<id>\d+)/delete/$',post_view.delete_post,name='delete'),
    url(r'^(?P<id>\d+)/like/$',post_view.like_post,name='like'),
    url(r'^(?P<id>\d+)/dislike/$',post_view.dislike_post,name='dislike'),
    url(r'^details/(?P<id>\d+)/$',post_view.post_details,name='details'),
    url(r'^details/(?P<id>\d+)/(?P<cid>\d+)/delete/$',post_view.delete_comment,name='deleteComment'),
    url(r'^details/(?P<id>\d+)/(?P<cid>\d+)/like/$',post_view.like_comment,name='likeComment'),
    url(r'^details/(?P<id>\d+)/(?P<cid>\d+)/dislike/$',post_view.dislike_comment,name='dislikeComment'),
    url(r'^create/', post_view.create_post, name='create'),
    url(r'^register/',account_view.register_view, name='signup'),
 	url(r'^login/',account_view.login_view, name='login'),
 	url(r'^logout/',account_view.logout_view, name='logout'),
 	url(r'^posts/',post_view.postList.as_view()), 
 	url(r'^profile/',account_view.profile, name='profile'),
 	url(r'^edit/',account_view.editProfile, name='editProfile'), 	
 	url(r'^notification/', post_view.notification, name='notification'),
 	url(r'^mail/', post_view.sendMail, name='mail'),
 	url(r'^(?P<id>\d+)/profile', account_view.userProfile, name='userProfile'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
